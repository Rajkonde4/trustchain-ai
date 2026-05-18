import { useState, useRef, useEffect } from "react"

import { useNavigate } from "react-router-dom"

import Navbar from "../components/Navbar"

export default function Upload() {

  const navigate = useNavigate()

  const API_URL = import.meta.env.VITE_API_URL

  const [selectedFile, setSelectedFile] = useState(null)

  const [isDragging, setIsDragging] = useState(false)

  const [isUploading, setIsUploading] = useState(false)

  const fileInputRef = useRef(null)

  // =========================
  // PROTECTED PAGE
  // =========================

  useEffect(() => {

    const token = localStorage.getItem(
      "token"
    )

    if (!token) {

      navigate("/login")
    }

  }, [])

  const fileType = selectedFile?.type

  // =========================
  // UPLOAD FUNCTION
  // =========================

  const uploadDocument = async (file) => {

    if (!file) return

    // =========================
    // FILE TYPE VALIDATION
    // =========================

    const allowedTypes = [

      "application/pdf",

      "image/png",

      "image/jpeg",

      "image/jpg"
    ]

    if (!allowedTypes.includes(file.type)) {

      alert(
        "Only PDF, PNG, JPG and JPEG files are allowed."
      )

      return
    }

    // =========================
    // FILE SIZE VALIDATION
    // =========================

    const maxSize = 10 * 1024 * 1024

    if (file.size > maxSize) {

      alert(
        "File size must be less than 10MB."
      )

      return
    }

    setSelectedFile(file)

    setIsUploading(true)

    try {

      const token = localStorage.getItem(
        "token"
      )

      const formData = new FormData()

      formData.append("file", file)

      const response = await fetch(

        `${API_URL}/upload`,

        {

          method: "POST",

          headers: {

            Authorization: `Bearer ${token}`
          },

          body: formData
        }
      )

      const data = await response.json()

      console.log(data)

      // =========================
      // FAILED RESPONSE
      // =========================

      if (!data.success) {

        // INVALID TOKEN
        if (

          data.message === "Unauthorized"

          || data.message === "Invalid Token"
        ) {

          alert("Please Login Again")

          localStorage.clear()

          navigate("/login")

          return
        }

        // OTHER ERRORS
        alert(data.message)

        setIsUploading(false)

        return
      }

      // =========================
      // SUCCESS
      // =========================

      navigate(
        `/result/${data.data.report_id}`
      )

    } catch (error) {

      console.log(error)

      alert(
        "Something went wrong while uploading the document."
      )

    } finally {

      setIsUploading(false)
    }
  }

  // =========================
  // FILE CHANGE
  // =========================

  const handleFileChange = async (event) => {

    const file = event.target.files[0]

    uploadDocument(file)
  }

  // =========================
  // DRAG OVER
  // =========================

  const handleDragOver = (event) => {

    event.preventDefault()

    setIsDragging(true)
  }

  // =========================
  // DRAG LEAVE
  // =========================

  const handleDragLeave = () => {

    setIsDragging(false)
  }

  // =========================
  // DROP FILE
  // =========================

  const handleDrop = async (event) => {

    event.preventDefault()

    setIsDragging(false)

    const file = event.dataTransfer.files[0]

    uploadDocument(file)
  }

  // =========================
  // REMOVE FILE
  // =========================

  const removeFile = () => {

    setSelectedFile(null)

    if (fileInputRef.current) {

      fileInputRef.current.value = ""
    }
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

            Detect fraud, analyze metadata,
            extract text using OCR,
            and generate AI-powered
            verification reports.

          </p>

        </div>

        {/* UPLOAD CARD */}
        <div className="mt-20 flex justify-center">

          <div

            className={`

              w-full
              max-w-4xl
              rounded-3xl
              p-14
              text-center
              shadow-xl
              transition
              hover:shadow-2xl
              hover:-translate-y-1
              border-2

              ${
                isDragging
                  ? "border-[#3B82F6] bg-blue-50"
                  : "bg-white border border-gray-200"
              }

            `}

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

              {
                isUploading
                  ? "Analyzing Document..."
                  : "Drag & Drop Documents"
              }

            </h2>

            {/* DESCRIPTION */}
            <p className="text-gray-500 mt-4">

              {
                isUploading

                  ? "OCR extraction, fraud analysis and intelligent verification in progress..."

                  : "Upload PDF, PNG, JPG, or scanned documents."
              }

            </p>

            {/* LOADING */}
            {

              isUploading && (

                <div className="mt-10 flex justify-center">

                  <div className="w-16 h-16 border-4 border-blue-200 border-t-[#3B82F6] rounded-full animate-spin"></div>

                </div>

              )
            }

            {/* BUTTON */}
            {

              !isUploading && (

                <label className="inline-block mt-10 bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-8 py-4 rounded-2xl font-medium text-lg shadow-lg cursor-pointer">

                  Browse Files

                  <input
                    type="file"
                    className="hidden"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                  />

                </label>

              )
            }

            {/* SELECTED FILE */}
            {

              selectedFile && !isUploading && (

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

      </div>

    </div>
  )
}