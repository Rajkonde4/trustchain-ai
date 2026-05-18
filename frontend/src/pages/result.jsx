import { useEffect, useState } from "react"

import {
  useNavigate,
  useParams
} from "react-router-dom"

import Navbar from "../components/Navbar"

export default function Result() {

  const { id } = useParams()

  const navigate = useNavigate()

  const [report, setReport] = useState(null)

  const [loading, setLoading] = useState(true)

  // =========================
  // FETCH REPORT
  // =========================

  useEffect(() => {

    const fetchReport = async () => {

      try {

        const token = localStorage.getItem(
          "token"
        )

        if (!token) {

          navigate("/login")

          return
        }

        const response = await fetch(

          `http://127.0.0.1:8000/report/${id}`,

          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        const data = await response.json()

        console.log(data)

        if (

          data.message === "Unauthorized"

          || data.message === "Invalid Token"

        ) {

          localStorage.clear()

          navigate("/login")

          return
        }

        setReport(data)

      } catch (error) {

        console.log(error)

      }

      setLoading(false)
    }

    fetchReport()

  }, [id])

  // =========================
  // LOADING
  // =========================

  if (loading) {

    return (

      <div className="min-h-screen flex items-center justify-center bg-[#F5F7FB]">

        <div className="text-3xl font-bold">

          Loading Report...

        </div>

      </div>
    )
  }

  // =========================
  // NO REPORT
  // =========================

  if (!report || report.message) {

    return (

      <div className="min-h-screen flex items-center justify-center bg-[#F5F7FB]">

        <div className="bg-white p-10 rounded-3xl shadow-xl text-center">

          <h1 className="text-4xl font-bold">
            Report Not Found
          </h1>

          <button

            onClick={() => navigate("/upload")}

            className="mt-6 bg-[#3B82F6] text-white px-6 py-3 rounded-2xl"
          >

            Upload Document

          </button>

        </div>

      </div>

    )
  }

  return (

    <div className="min-h-screen bg-[#F5F7FB] text-[#111827]">

      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-14">

        {/* HEADER */}
        <div className="text-center">

          <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
            AI Verification Result
          </p>

          <h1 className="text-6xl font-bold mt-6">
            Document Analysis Report
          </h1>

          <p className="text-gray-500 text-xl mt-6 max-w-3xl mx-auto">
            AI-powered fraud analysis, OCR extraction,
            metadata verification and intelligent document insights.
          </p>

        </div>

        {/* TOP CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-14">

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200">

            <p className="text-gray-500">
              Document Type
            </p>

            <h2 className="text-3xl font-bold mt-4">
              {report.document_category}
            </h2>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200">

            <p className="text-gray-500">
              Fraud Risk
            </p>

            <h2 className={`text-3xl font-bold mt-4

              ${
                report.fraud_risk === "Low"
                  ? "text-green-500"
                  : report.fraud_risk === "Medium"
                  ? "text-yellow-500"
                  : "text-red-500"
              }
            `}>

              {report.fraud_risk}

            </h2>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200">

            <p className="text-gray-500">
              Confidence Score
            </p>

            <h2 className="text-3xl font-bold mt-4 text-[#3B82F6]">
              {report.confidence_score}%
            </h2>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200">

            <p className="text-gray-500">
              Verification Status
            </p>

            <h2 className="text-2xl font-bold mt-4">
              {report.verification_status}
            </h2>

          </div>

        </div>

        {/* OCR TEXT */}
        <div className="mt-14 bg-white rounded-3xl shadow-sm border border-gray-200 p-10">

          <h2 className="text-4xl font-bold">
            OCR Extracted Text
          </h2>

          <div className="mt-8 bg-gray-50 rounded-2xl p-6 max-h-[500px] overflow-y-auto whitespace-pre-wrap text-gray-700 leading-relaxed">

            {report.extracted_text}

          </div>

        </div>

        {/* ACTIONS */}
        <div className="flex flex-wrap gap-6 mt-14">

          <button

            onClick={() => {

              window.open(

                `http://127.0.0.1:8000/download-report/${id}`,

                "_blank"
              )
            }}

            className="bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-8 py-4 rounded-2xl font-semibold shadow-lg"
          >

            Download Report

          </button>

          <button

            onClick={() => {

              window.open(

                `http://localhost:5173/verify/${id}`,

                "_blank"
              )
            }}

            className="bg-white border border-gray-200 px-8 py-4 rounded-2xl font-semibold shadow-sm"
          >

            Public Verification

          </button>

        </div>

      </div>

    </div>
  )
}