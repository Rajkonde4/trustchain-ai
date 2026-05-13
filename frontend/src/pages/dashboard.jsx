import { useEffect, useState } from "react"
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

  const [reports, setReports] = useState([])

  useEffect(() => {

    fetch("http://127.0.0.1:8000/reports")

      .then((res) => res.json())

      .then((data) => {

        console.log(data)

        setReports(data)

      })

  }, [])

  // REAL ANALYTICS
  const totalUploads = reports.length

  const fraudDetected = reports.filter(
    (report) => report.fraud_risk === "High"
  ).length

  const verifiedDocuments = reports.filter(
    (report) => report.fraud_risk === "Low"
  ).length

  const accuracyRate =
    totalUploads > 0
      ? Math.round((verifiedDocuments / totalUploads) * 100)
      : 0

  // CHART DATA
  const fraudData = [
    { month: "Jan", fraud: 12 },
    { month: "Feb", fraud: 19 },
    { month: "Mar", fraud: 8 },
    { month: "Apr", fraud: 15 },
    { month: "May", fraud: 10 },
    { month: "Jun", fraud: 6 },
  ]

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

            <div className="bg-blue-50 text-[#3B82F6] px-5 py-4 rounded-2xl font-medium">
              Overview
            </div>

            <div className="text-gray-600 px-5 py-4 rounded-2xl hover:bg-gray-100 transition cursor-pointer">
              Uploads
            </div>

            <div className="text-gray-600 px-5 py-4 rounded-2xl hover:bg-gray-100 transition cursor-pointer">
              Reports
            </div>

            <div className="text-gray-600 px-5 py-4 rounded-2xl hover:bg-gray-100 transition cursor-pointer">
              Fraud Analysis
            </div>

            <div className="text-gray-600 px-5 py-4 rounded-2xl hover:bg-gray-100 transition cursor-pointer">
              Settings
            </div>

          </div>

        </div>

        {/* MAIN CONTENT */}
        <div className="flex-1 p-10">

          {/* HEADER */}
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">

            <div>

              <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
                Analytics Dashboard
              </p>

              <h1 className="text-5xl font-bold mt-4">
                Verification Overview
              </h1>

            </div>

            <button className="bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-6 py-4 rounded-2xl font-medium shadow-lg">
              Generate Report
            </button>

          </div>

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

          {/* ANALYTICS CHART */}
          <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

            <div className="flex items-center justify-between mb-8">

              <div>

                <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
                  Analytics
                </p>

                <h2 className="text-3xl font-bold mt-3">
                  Fraud Detection Trends
                </h2>

              </div>

            </div>

            <div className="w-full h-[350px] min-w-0">

              <ResponsiveContainer width="100%" height="100%">

                <LineChart data={fraudData}>

                  <XAxis dataKey="month" />

                  <YAxis />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="fraud"
                    stroke="#3B82F6"
                    strokeWidth={4}
                  />

                </LineChart>

              </ResponsiveContainer>

            </div>

          </div>

          {/* RECENT UPLOADS */}
          <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

            <div className="flex items-center justify-between">

              <h2 className="text-2xl font-bold">
                Recent Uploads
              </h2>

            </div>

            <div className="mt-8 overflow-x-auto">

              <table className="w-full">

                <thead>

                  <tr className="text-left text-gray-500 border-b border-gray-100">

                    <th className="pb-4">Document</th>
                    <th className="pb-4">Category</th>
                    <th className="pb-4">Risk</th>
                    <th className="pb-4">Score</th>

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

          </div>

        </div>

      </div>

    </div>
  )
}