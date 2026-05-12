import { useState } from "react"
import Navbar from "../components/Navbar"

export default function Upload() {

  const [selectedFile, setSelectedFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)

  const fileType = selectedFile?.type

  const handleFileChange = (event) => {
    const file = event.target.files[0]

    if (file) {
      setSelectedFile(file)
    }
  }

  const handleDragOver = (event) => {
    event.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (event) => {
    event.preventDefault()

    setIsDragging(false)

    const file = event.dataTransfer.files[0]

    if (file) {
      setSelectedFile(file)
    }
  }

  const removeFile = () => {
    setSelectedFile(null)
  }

  return (
    <div className="min-h-screen bg-[#F5F7FB] text-[#111827]">

      <Navbar />

      <div className="max-w-6xl mx-auto px-6 pt-24">

        {/* HEADER */}
        <div className="text-center">

          <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
            AI Verification Platform
          </p>

          <h1 className="text-5xl md:text-6xl font-bold mt-6 leading-tight">
            Upload Documents
            <br />
            For Intelligent Verification
          </h1>

          <p className="text-gray-500 mt-6 text-lg max-w-2xl mx-auto leading-relaxed">
            Detect fraud, analyze metadata, extract text using OCR,
            and generate AI-powered verification reports.
          </p>

        </div>

        {/* UPLOAD CARD */}
        <div className="mt-20 flex justify-center">

          <div
            className={`w-full max-w-4xl rounded-3xl p-14 text-center shadow-xl transition hover:shadow-2xl hover:-translate-y-1 border-2 ${
              isDragging
                ? "border-[#3B82F6] bg-blue-50"
                : "bg-white border border-gray-200"
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >

            {/* ICON */}
            <div className="w-20 h-20 rounded-2xl bg-blue-50 flex items-center justify-center mx-auto mb-8">

              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-10 h-10 text-[#3B82F6]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M7 16V4m0 0L3 8m4-4l4 4m6 8v4m0 0l4-4m-4 4l-4-4"
                />
              </svg>

            </div>

            {/* TITLE */}
            <h2 className="text-3xl font-semibold text-[#111827]">
              Drag & Drop Documents
            </h2>

            {/* DESCRIPTION */}
            <p className="text-gray-500 mt-4">
              Upload PDF, PNG, JPG, or scanned documents.
            </p>

            {/* BUTTON */}
            <label className="inline-block mt-10 bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-8 py-4 rounded-2xl font-medium text-lg shadow-lg cursor-pointer">

              Browse Files

              <input
                type="file"
                className="hidden"
                onChange={handleFileChange}
              />

            </label>

            {/* SELECTED FILE */}
            {
              selectedFile && (

                <div className="mt-8 bg-blue-50 border border-blue-100 rounded-2xl px-6 py-5">

                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">

                    <div className="text-left">

                      <p className="text-lg font-semibold text-[#111827] break-all">
                        {selectedFile.name}
                      </p>

                      <p className="text-sm text-gray-500 mt-1">
                        {fileType}
                      </p>

                    </div>

                    <div className="flex items-center gap-3">

                      <div className="bg-white border border-blue-200 text-[#3B82F6] px-4 py-2 rounded-xl text-sm font-medium shadow-sm">

                        {
                          fileType?.includes("pdf")
                            ? "PDF Document"
                            : fileType?.includes("image")
                            ? "Image File"
                            : "Document"
                        }

                      </div>

                      <button
                        onClick={removeFile}
                        className="bg-red-50 hover:bg-red-100 text-red-500 px-4 py-2 rounded-xl text-sm font-medium transition"
                      >
                        Remove
                      </button>

                    </div>

                  </div>

                </div>

              )
            }

          </div>

        </div>

        {/* FEATURES */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 pb-32">

          <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm hover:shadow-md transition">

            <h3 className="text-xl font-semibold text-[#111827]">
              OCR Analysis
            </h3>

            <p className="text-gray-500 mt-4 leading-relaxed">
              Extract and analyze text from scanned and digital documents.
            </p>

          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm hover:shadow-md transition">

            <h3 className="text-xl font-semibold text-[#111827]">
              Fraud Detection
            </h3>

            <p className="text-gray-500 mt-4 leading-relaxed">
              Detect edited regions, suspicious metadata, and forged elements.
            </p>

          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm hover:shadow-md transition">

            <h3 className="text-xl font-semibold text-[#111827]">
              Verification Reports
            </h3>

            <p className="text-gray-500 mt-4 leading-relaxed">
              Generate intelligent fraud analysis and authenticity reports.
            </p>

          </div>

        </div>

      </div>

    </div>
  )
}