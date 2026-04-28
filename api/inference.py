from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import models, transforms

from logger import get_logger

CLASS_NAMES = [
    "No Dementia",
    "Very Mild Dementia",
    "Mild Dementia",
    "Moderate Dementia",
]

ROOT_DIR = Path(__file__).resolve().parents[1]

MODEL_CONFIGS = {
    "SNNCap V1": {
        "model_path": ROOT_DIR / "SNNCap_v1.0" / "siamese_capsule_alzheimer_4class.pth",
        "ref_path": ROOT_DIR / "SNNCap_v1.0" / "reference_embeddings_means.pt",
    },
    "SNNCap V2": {
        "model_path": ROOT_DIR / "SNNCap_v2.0" / "siamese_capsule_finetuned.pth",
        "ref_path": ROOT_DIR / "SNNCap_v2.0" / "reference_embeddings_means_finetuned.pt",
    },
}

MODEL_LABELS = list(MODEL_CONFIGS.keys())
MODEL_KEYS = set(MODEL_CONFIGS.keys())


class ResizeWithPadding:
    def __init__(self, target_size):
        self.target_size = target_size

    def __call__(self, image):
        width, height = image.size
        ratio = min(self.target_size[1] / width, self.target_size[0] / height)
        new_w, new_h = int(width * ratio), int(height * ratio)
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        new_img = Image.new("L", self.target_size, color=0)
        new_img.paste(
            image,
            (
                (self.target_size[1] - new_w) // 2,
                (self.target_size[0] - new_h) // 2,
            ),
        )
        return new_img


def build_transform():
    return transforms.Compose(
        [
            ResizeWithPadding((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5]),
        ]
    )


class PrimaryCapsules(nn.Module):
    def __init__(self, in_ch, out_ch, k, s, p, n_caps, cap_dim):
        super().__init__()
        self.num_capsules = n_caps
        self.capsule_dim = cap_dim
        self.conv = nn.Conv2d(in_ch, out_ch, kernel_size=k, stride=s, padding=p)
        self.relu = nn.ReLU(inplace=True)

    def squash(self, t, dim=-1):
        s2 = (t**2).sum(dim=dim, keepdim=True)
        scale = s2 / (1 + s2)
        return scale * t / torch.sqrt(s2 + 1e-8)

    def forward(self, x):
        batch = x.size(0)
        out = self.relu(self.conv(x))
        out = (
            out.view(batch, self.num_capsules, self.capsule_dim, -1)
            .permute(0, 3, 1, 2)
            .contiguous()
        )
        out = out.view(batch, -1, self.capsule_dim)
        return self.squash(out)


class DigitCapsules(nn.Module):
    def __init__(self, num_caps, in_caps, in_dim, out_dim, iters=3):
        super().__init__()
        self.num_capsules = num_caps
        self.iters = iters
        self.W = nn.Parameter(0.01 * torch.randn(1, in_caps, num_caps, out_dim, in_dim))

    def squash(self, t, dim=-1):
        s2 = (t**2).sum(dim=dim, keepdim=True)
        scale = s2 / (1 + s2)
        return scale * t / torch.sqrt(s2 + 1e-8)

    def forward(self, x):
        batch = x.size(0)
        x = x.unsqueeze(2).unsqueeze(4)
        W = self.W.repeat(batch, 1, 1, 1, 1)
        u_hat = torch.matmul(W, x).squeeze(-1)
        b_ij = torch.zeros(batch, u_hat.size(1), u_hat.size(2), 1, device=x.device)
        for _ in range(self.iters):
            c_ij = F.softmax(b_ij, dim=2)
            s_j = (c_ij * u_hat).sum(dim=1, keepdim=True)
            v_j = self.squash(s_j, dim=-1)
            b_ij = b_ij + (u_hat * v_j).sum(dim=-1, keepdim=True)
        return v_j.squeeze(1)


class CapsuleNetwork(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        backbone = models.resnet18(weights=None)
        backbone.conv1 = nn.Conv2d(1, 64, 7, 2, 3, bias=False)
        self.cnn = nn.Sequential(*list(backbone.children())[:-2])
        self.primary = PrimaryCapsules(512, 256, 3, 1, 1, n_caps=32, cap_dim=8)
        self.digit = DigitCapsules(num_classes, 32 * 7 * 7, 8, 16)

    def forward(self, x):
        x = self.cnn(x)
        x = self.primary(x)
        x = self.digit(x)
        return x.norm(dim=-1)


class SiameseCapsuleNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.capsule_net = CapsuleNetwork()

    def forward(self, x1, x2):
        e1 = self.capsule_net(x1)
        e2 = self.capsule_net(x2)
        return torch.norm(e1 - e2, dim=1, keepdim=True)


class ModelRegistry:
    def __init__(self):
        self.device = torch.device("cpu")
        self.transform = build_transform()
        self._models = {}
        self._refs = {}
        self.logger = get_logger("inference", "inference.log")

    def _normalize_state_dict(self, state_dict):
        remap = {
            "capsule_net.primary_capsules.": "capsule_net.primary.",
            "capsule_net.digit_capsules.": "capsule_net.digit.",
        }
        updated = {}
        for key, value in state_dict.items():
            new_key = key
            for old, new in remap.items():
                if new_key.startswith(old):
                    new_key = new + new_key[len(old) :]
                    break
            updated[new_key] = value
        return updated

    def _load_model(self, model_key):
        config = MODEL_CONFIGS[model_key]
        model = SiameseCapsuleNetwork().to(self.device)
        model_path = Path(config["model_path"])
        if not model_path.exists():
            self.logger.error("Model file not found: %s", model_path)
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.logger.info("Loading model: %s", model_path)
        obj = torch.load(str(model_path), map_location=self.device)
        state_dict = obj["model_state_dict"] if isinstance(obj, dict) else obj
        if any(
            key.startswith("capsule_net.primary_capsules.")
            or key.startswith("capsule_net.digit_capsules.")
            for key in state_dict.keys()
        ):
            self.logger.info("Remapping legacy state_dict keys")
            state_dict = self._normalize_state_dict(state_dict)

        try:
            model.load_state_dict(state_dict, strict=True)
        except RuntimeError as exc:
            self.logger.warning("Strict load failed: %s", exc)
            result = model.load_state_dict(state_dict, strict=False)
            self.logger.warning(
                "Loaded with strict=False. Missing: %s Unexpected: %s",
                result.missing_keys,
                result.unexpected_keys,
            )
        model.eval()
        return model

    def _load_reference(self, model_key):
        config = MODEL_CONFIGS[model_key]
        ref_path = Path(config["ref_path"])
        if not ref_path.exists():
            self.logger.error("Reference file not found: %s", ref_path)
            raise FileNotFoundError(f"Reference file not found: {ref_path}")
        self.logger.info("Loading reference: %s", ref_path)
        reference_embeddings = torch.load(str(ref_path), map_location=self.device)
        cleaned = {}
        for k, v in list(reference_embeddings.items()):
            cleaned[int(k)] = [t.to(self.device).float().view(-1) for t in v]
        return cleaned

    def _ensure_loaded(self, model_key):
        if model_key not in self._models:
            self._models[model_key] = self._load_model(model_key)
        if model_key not in self._refs:
            self._refs[model_key] = self._load_reference(model_key)

    @torch.no_grad()
    def predict(self, img, model_key):
        self._ensure_loaded(model_key)
        model = self._models[model_key]
        references = self._refs[model_key]

        img = img.convert("L")
        x = self.transform(img).unsqueeze(0).to(self.device)
        test_vec = model.capsule_net(x).squeeze(0)

        d_means = []
        for cls in range(4):
            vectors = references[cls]
            ds = [
                F.pairwise_distance(test_vec.unsqueeze(0), r.unsqueeze(0), p=2).item()
                for r in vectors
            ]
            d_means.append(float(sum(ds) / len(ds)))

        inv = 1.0 / (torch.tensor(d_means) + 1e-8)
        close = (100.0 * (inv / inv.sum())).tolist()
        pred = int(torch.argmin(torch.tensor(d_means)))

        bars = {CLASS_NAMES[i]: close[i] for i in range(4)}
        return {
            "model_version": model_key,
            "predicted_class": CLASS_NAMES[pred],
            "closeness": bars,
            "distances": d_means,
        }


_registry = None


def get_registry():
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
