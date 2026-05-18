import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

import Navbar from "../components/Navbar"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts"

export default function Dashboard() {

  const navigate = useNavigate()

  const API_URL = import.meta.env.VITE_API_URL

  const FRONTEND_URL =
    import.meta.env.VITE_FRONTEND_URL

  const [reports, setReports] = useState([])

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState("")

  const [activeSection, setActiveSection] = useState(
    "overview"
  )

  // =========================
  // AUTH + FETCH REPORTS
  // =========================

  useEffect(() => {

    const token = localStorage.getItem(
      "token"
    )

    // NO TOKEN
    if (!token) {

      navigate("/login")

      return
    }

    fetch(
      `${API_URL}/reports`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

      .then((res) => res.json())

      .then((data) => {

        console.log(data)

        if (
          data.message === "Unauthorized"
          || data.message === "Invalid Token"
        ) {

          localStorage.clear()

          navigate("/login")

          return
        }

        setReports(data)

        setLoading(false)

      })

      .catch((error) => {

        console.log(error)

        setError(
          "Failed to load dashboard data."
        )

        setLoading(false)

      })

  }, [navigate, API_URL])

  // =========================
  // ANALYTICS
  // =========================

  const totalUploads = reports.length

  const fraudDetected = reports.filter(
    (report) => report.fraud_risk === "High"
  ).length

  const verifiedDocuments = reports.filter(
    (report) => report.fraud_risk === "Low"
  ).length

  const accuracyRate =
    totalUploads > 0
      ? Math.round(
          (verifiedDocuments / totalUploads) * 100
        )
      : 0

  // =========================
  // REAL CHART DATA
  // =========================

  const fraudData = [

    {
      risk: "Low",
      count: reports.filter(
        (report) => report.fraud_risk === "Low"
      ).length
    },

    {
      risk: "Medium",
      count: reports.filter(
        (report) => report.fraud_risk === "Medium"
      ).length
    },

    {
      risk: "High",
      count: reports.filter(
        (report) => report.fraud_risk === "High"
      ).length
    }

  ]

  // =========================
  // LOGOUT
  // =========================

  const handleLogout = () => {

    localStorage.clear()

    navigate("/login")
  }

  // =========================
  // LOADING
  // =========================

  if (loading) {

    return (

      <div className="min-h-screen flex items-center justify-center bg-[#F5F7FB]">

        <div className="text-3xl font-bold">

          Loading Dashboard...

        </div>

      </div>
    )
  }

  // =========================
  // ERROR
  // =========================

  if (error) {

    return (

      <div className="min-h-screen flex items-center justify-center bg-[#F5F7FB]">

        <div className="bg-white p-10 rounded-3xl shadow-xl text-center">

          <h1 className="text-4xl font-bold text-red-500">
            Error
          </h1>

          <p className="mt-4 text-gray-500">
            {error}
          </p>

        </div>

      </div>
    )
  }

  return (

    <div className="min-h-screen bg-[#F5F7FB] text-[#111827]">

      <Navbar />

      <div className="flex">

        {/* SIDEBAR */}
        <div className="w-[260px] min-h-screen bg-white border-r border-gray-200 p-8 hidden lg:block">

          <h2 className="text-2xl font-bold">
            Dashboard
          </h2>

          <div className="mt-10 space-y-4">

            {/* OVERVIEW */}
            <div

              onClick={() => setActiveSection("overview")}

              className={`px-5 py-4 rounded-2xl font-medium cursor-pointer transition

                ${
                  activeSection === "overview"
                    ? "bg-blue-50 text-[#3B82F6]"
                    : "text-gray-600 hover:bg-gray-100"
                }
              `}
            >

              Overview

            </div>

            {/* UPLOAD HISTORY */}
            <div

              onClick={() => setActiveSection("uploads")}

              className={`px-5 py-4 rounded-2xl font-medium cursor-pointer transition

                ${
                  activeSection === "uploads"
                    ? "bg-blue-50 text-[#3B82F6]"
                    : "text-gray-600 hover:bg-gray-100"
                }
              `}
            >

              Upload History

            </div>

            {/* REPORTS */}
            <div

              onClick={() => setActiveSection("reports")}

              className={`px-5 py-4 rounded-2xl font-medium cursor-pointer transition

                ${
                  activeSection === "reports"
                    ? "bg-blue-50 text-[#3B82F6]"
                    : "text-gray-600 hover:bg-gray-100"
                }
              `}
            >

              Reports

            </div>

            {/* ANALYTICS */}
            <div

              onClick={() => setActiveSection("analytics")}

              className={`px-5 py-4 rounded-2xl font-medium cursor-pointer transition

                ${
                  activeSection === "analytics"
                    ? "bg-blue-50 text-[#3B82F6]"
                    : "text-gray-600 hover:bg-gray-100"
                }
              `}
            >

              Fraud Analytics

            </div>

            {/* SETTINGS */}
            <div

              onClick={() => setActiveSection("settings")}

              className={`px-5 py-4 rounded-2xl font-medium cursor-pointer transition

                ${
                  activeSection === "settings"
                    ? "bg-blue-50 text-[#3B82F6]"
                    : "text-gray-600 hover:bg-gray-100"
                }
              `}
            >

              Settings

            </div>

          </div>

        </div>

        {/* MAIN CONTENT */}
        <div className="flex-1 p-10">

          {/* HEADER */}
          <div>

            <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
              Analytics Dashboard
            </p>

            <h1 className="text-5xl font-bold mt-4">

              {
                activeSection === "overview"
                  ? "Verification Overview"
                  : activeSection === "uploads"
                  ? "Upload History"
                  : activeSection === "reports"
                  ? "Reports Center"
                  : activeSection === "analytics"
                  ? "Fraud Analytics"
                  : "Settings"
              }

            </h1>

            <p className="text-gray-500 mt-4">

              Monitor uploaded documents, fraud detection,
              and verification analytics.

            </p>

          </div>

          {/* ========================= */}
          {/* OVERVIEW */}
          {/* ========================= */}

          {
            activeSection === "overview" && (

              <>

                {/* STATS */}
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mt-12">

                  <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

                    <p className="text-gray-500">
                      Total Uploads
                    </p>

                    <h2 className="text-4xl font-bold mt-4">
                      {totalUploads}
                    </h2>

                  </div>

                  <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

                    <p className="text-gray-500">
                      Fraud Detected
                    </p>

                    <h2 className="text-4xl font-bold mt-4 text-red-500">
                      {fraudDetected}
                    </h2>

                  </div>

                  <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

                    <p className="text-gray-500">
                      Verified Documents
                    </p>

                    <h2 className="text-4xl font-bold mt-4 text-green-500">
                      {verifiedDocuments}
                    </h2>

                  </div>

                  <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

                    <p className="text-gray-500">
                      Accuracy Rate
                    </p>

                    <h2 className="text-4xl font-bold mt-4 text-[#3B82F6]">
                      {accuracyRate}%
                    </h2>

                  </div>

                </div>

                {/* CHART */}
                <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

                  <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
                    Fraud Analytics
                  </p>

                  <h2 className="text-3xl font-bold mt-3">
                    Fraud Risk Distribution
                  </h2>

                  <div className="w-full h-[350px] mt-10">

                    <ResponsiveContainer width="100%" height="100%">

                      <LineChart data={fraudData}>

                        <XAxis dataKey="risk" />

                        <YAxis />

                        <Tooltip />

                        <Line
                          type="monotone"
                          dataKey="count"
                          stroke="#3B82F6"
                          strokeWidth={4}
                        />

                      </LineChart>

                    </ResponsiveContainer>

                  </div>

                </div>

              </>

            )
          }

          {/* ========================= */}
          {/* UPLOAD HISTORY */}
          {/* ========================= */}

          {
            activeSection === "uploads" && (

              <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

                <h2 className="text-2xl font-bold">
                  Uploaded Documents
                </h2>

                {
                  reports.length === 0 && (

                    <div className="text-center py-16">

                      <h2 className="text-3xl font-bold">
                        No Uploads Yet
                      </h2>

                      <p className="text-gray-500 mt-4">
                        Upload documents to view analytics.
                      </p>

                    </div>
                  )
                }

                {
                  reports.length > 0 && (

                    <div className="mt-8 overflow-x-auto">

                      <table className="w-full">

                        <thead>

                          <tr className="text-left text-gray-500 border-b border-gray-100">

                            <th className="pb-4">
                              Document
                            </th>

                            <th className="pb-4">
                              Category
                            </th>

                            <th className="pb-4">
                              Risk
                            </th>

                            <th className="pb-4">
                              Score
                            </th>

                          </tr>

                        </thead>

                        <tbody>

                          {
                            reports.map((report) => (

                              <tr
                                key={report._id}
                                className="border-b border-gray-100"
                              >

                                <td className="py-5">
                                  {report.filename}
                                </td>

                                <td className="py-5">
                                  {report.document_category}
                                </td>

                                <td className="py-5">

                                  <span
                                    className={`px-4 py-2 rounded-xl text-sm font-medium

                                      ${
                                        report.fraud_risk === "Low"
                                          ? "bg-green-100 text-green-600"
                                          : report.fraud_risk === "Medium"
                                          ? "bg-yellow-100 text-yellow-600"
                                          : "bg-red-100 text-red-600"
                                      }
                                    `}
                                  >

                                    {report.fraud_risk}

                                  </span>

                                </td>

                                <td className="py-5">
                                  {report.confidence_score}%
                                </td>

                              </tr>

                            ))
                          }

                        </tbody>

                      </table>

                    </div>
                  )
                }

              </div>

            )
          }

          {/* ========================= */}
          {/* REPORTS */}
          {/* ========================= */}

          {
            activeSection === "reports" && (

              <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

                <h2 className="text-2xl font-bold">
                  Reports Center
                </h2>

                {
                  reports.length === 0 && (

                    <div className="text-center py-16">

                      <h2 className="text-3xl font-bold">
                        No Reports Available
                      </h2>

                      <p className="text-gray-500 mt-4">
                        Upload documents to generate reports.
                      </p>

                    </div>
                  )
                }

                {
                  reports.length > 0 && (

                    <div className="mt-8 space-y-5">

                      {
                        reports.map((report) => (

                          <div
                            key={report._id}
                            className="border border-gray-200 rounded-2xl p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-5"
                          >

                            <div>

                              <h3 className="text-xl font-semibold">
                                {report.filename}
                              </h3>

                              <p className="text-gray-500 mt-2">
                                {report.document_category}
                              </p>

                            </div>

                            <div className="flex gap-4">

                              <button

                                onClick={() => {

                                  window.open(

                                    `${API_URL}/download-report/${report._id}`,

                                    "_blank"
                                  )
                                }}

                                className="bg-[#3B82F6] hover:bg-[#2563EB] text-white px-5 py-3 rounded-2xl font-medium transition"
                              >

                                Download

                              </button>

                              <button

                                onClick={() => {

                                  window.open(

                                    `${FRONTEND_URL}/verify/${report._id}`,

                                    "_blank"
                                  )
                                }}

                                className="bg-gray-100 hover:bg-gray-200 px-5 py-3 rounded-2xl font-medium transition"
                              >

                                Verify

                              </button>

                            </div>

                          </div>

                        ))
                      }

                    </div>
                  )
                }

              </div>

            )
          }

          {/* ========================= */}
          {/* ANALYTICS */}
          {/* ========================= */}

          {
            activeSection === "analytics" && (

              <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

                <h2 className="text-3xl font-bold">
                  Fraud Analytics
                </h2>

                <div className="w-full h-[400px] mt-10">

                  <ResponsiveContainer width="100%" height="100%">

                    <LineChart data={fraudData}>

                      <XAxis dataKey="risk" />

                      <YAxis />

                      <Tooltip />

                      <Line
                        type="monotone"
                        dataKey="count"
                        stroke="#3B82F6"
                        strokeWidth={4}
                      />

                    </LineChart>

                  </ResponsiveContainer>

                </div>

              </div>

            )
          }

          {/* ========================= */}
          {/* SETTINGS */}
          {/* ========================= */}

          {
            activeSection === "settings" && (

              <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

                <h2 className="text-3xl font-bold">
                  Settings
                </h2>

                <div className="mt-8">

                  <button

                    onClick={handleLogout}

                    className="bg-red-500 hover:bg-red-600 transition text-white px-8 py-4 rounded-2xl font-semibold"
                  >

                    Logout

                  </button>

                </div>

              </div>

            )
          }

        </div>

      </div>

    </div>
  )
}