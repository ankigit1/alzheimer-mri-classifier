// MRIUpload.jsx
import { useState, useRef } from "react";
import { Upload, Image as ImageIcon, X, Brain, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from "recharts";

// ✅ The API URL now points to your local server
const API_URL = "http://localhost:5000/analyse_mri";

export default function MRIUpload({ onImageSelect, selectedImage, isLoading, prediction }) {
  const [dragActive, setDragActive] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const fileInputRef = useRef(null);

  // --- API call handler (handled by parent) ---
  // analyzeMRI is called from parent via props



  // --- UI handlers (unchanged) ---
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
    else if (e.type === "dragleave") setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleFiles = (files) => {
    if (!files?.length) return;
    const file = files[0];
    if (!file.type.startsWith("image/")) {
      toast.error("Please select a valid image file");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      toast.error("File must be less than 10MB");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => setPreviewUrl(e.target?.result || null);
    reader.readAsDataURL(file);

    onImageSelect(file);
  };

  const clearImage = () => {
    setPreviewUrl(null);
    onImageSelect(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  // --- render (unchanged, with updated onClick) ---
  return (
    <div className=" flex items-center justify-center p-8">
      <div className="w-full max-w-5xl mx-auto space-y-6">
        {!selectedImage && (
          <Card className="bg-white border border-gray-300 shadow-md">
            <CardContent className="p-8">
              <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${
                  dragActive
                    ? "border-blue-500 bg-blue-50 scale-105"
                    : "border-gray-300 hover:border-blue-300 hover:bg-gray-50"
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".jpg,.jpeg,.png"
                  onChange={(e) => handleFiles(e.target.files)}
                  className="hidden"
                />
                <div className="space-y-4">
                  <div className="mx-auto w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center shadow-md">
                    <Upload className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Upload MRI Scan
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Drag and drop your MRI image here, or click to browse
                  </p>
                  <Button
                    onClick={() => fileInputRef.current?.click()}
                    className="bg-blue-500 text-white hover:bg-blue-600"
                  >
                    <ImageIcon className="w-4 h-4 mr-2" />
                    Select MRI Image
                  </Button>
                  <div className="text-xs text-gray-500">
                    Supports JPG, JPEG, PNG • Max 10MB
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {selectedImage && previewUrl && (
          <Card className="bg-white border border-gray-300 shadow-md">
            <CardContent className="p-6 flex flex-col space-y-6">
              {/* Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center shadow-md">
                    <Brain className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      MRI Analysis
                    </h3>
                    <p className="text-sm text-gray-600">{selectedImage.name}</p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearImage}
                  className="border-gray-300 text-gray-600 hover:bg-red-50 hover:text-red-500"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              {/* MRI Preview */}
              <div className="relative overflow-hidden rounded-lg bg-gray-50">
                <img
                  src={previewUrl}
                  alt="MRI Preview"
                  className="w-full h-64 object-contain"
                />
              </div>

              {/* Analyze Button - handled by parent */}
              {/* This section is handled by parent component (Index.jsx) */}

              {/* Loading State */}
              {isLoading && (
                <div className="flex items-center justify-center space-x-3 text-blue-600">
                  <Loader2 className="w-6 h-6 animate-spin" />
                  <span className="font-medium">Analyzing MRI...</span>
                </div>
              )}

              {/* Results - only appear when prediction exists */}
              {prediction && (
                <>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 text-center">
                    <h4 className="text-gray-600 text-sm uppercase tracking-wide">
                      Predicted Class
                    </h4>
                    <p className="text-2xl font-bold text-blue-600">
                      {prediction.class}
                    </p>
                  </div>
                  {prediction && (
                    <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <h4 className="text-gray-600 text-sm uppercase tracking-wide mb-4">
                        Class Closeness
                      </h4>
          <ResponsiveContainer width="100%" height={380}>
            <BarChart
              data={prediction.closeness.map(d => ({
                Class: d.class,
                "Closeness (%)": d.score
              }))}
              margin={{ top: 20, right: 30, left: 20, bottom: 90 }}
            >
              {/* Define gradient for bar fill */}
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.9} />
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0.7} />
                </linearGradient>
                <linearGradient id="otherGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.9} />
                  <stop offset="95%" stopColor="#ea580c" stopOpacity={0.7} />
                </linearGradient>
              </defs>

              <XAxis
                dataKey="Class"
                angle={-25}
                textAnchor="end"
                interval={0}
                tick={{ fontSize: 14, fill: "#374151" }}
                label={{
                  value: "Class Categories",
                  position: "insideBottom",
                  offset: -70,
                  style: { fontSize: 14, fill: "#4b5563" },
                }}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 14, fill: "#374151" }}
                label={{
                  value: "Closeness (%)",
                  angle: -90,
                  position: "insideLeft",
                  style: { textAnchor: "middle", fontSize: 14, fill: "#4b5563" },
                }}
              />
              <Tooltip
                formatter={(v) => `${v.toFixed(2)}%`}
                contentStyle={{
                  backgroundColor: "#ffffff",
                  borderRadius: "10px",
                  boxShadow: "0px 2px 8px rgba(0,0,0,0.15)",
                  border: "1px solid #e5e7eb",
                }}
              />
              <Bar
                dataKey="Closeness (%)"
                radius={[10, 10, 0, 0]}
                animationDuration={1200}
                animationEasing="ease-out"
              >
                <LabelList
                  dataKey="Closeness (%)"
                  position="top"
                  formatter={(v) => `${v.toFixed(0)}%`}
                  style={{ fontWeight: "600", fill: "#111827" }}
                />
                {prediction.closeness.map((entry, i) => (
                  <Cell
                    key={`cell-${i}`}
                    fill={
                      entry.class === prediction.class
                        ? "url(#barGradient)"
                        : "url(#otherGradient)"
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
                    </div>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}