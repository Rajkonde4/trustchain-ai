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
                1,284
              </h2>

            </div>

            <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

              <p className="text-gray-500">
                Fraud Detected
              </p>

              <h2 className="text-4xl font-bold mt-4 text-red-500">
                87
              </h2>

            </div>

            <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

              <p className="text-gray-500">
                Verified Documents
              </p>

              <h2 className="text-4xl font-bold mt-4 text-green-500">
                1,197
              </h2>

            </div>

            <div className="bg-white p-8 rounded-3xl border border-gray-200 shadow-sm">

              <p className="text-gray-500">
                Accuracy Rate
              </p>

              <h2 className="text-4xl font-bold mt-4 text-[#3B82F6]">
                99%
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

          {/* RECENT ACTIVITY */}
          <div className="mt-12 bg-white rounded-3xl border border-gray-200 shadow-sm p-8">

            <div className="flex items-center justify-between">

              <h2 className="text-2xl font-bold">
                Recent Uploads
              </h2>

              <button className="text-[#3B82F6] font-medium">
                View All
              </button>

            </div>

            <div className="mt-8 overflow-x-auto">

              <table className="w-full">

                <thead>

                  <tr className="text-left text-gray-500 border-b border-gray-100">

                    <th className="pb-4">Document</th>
                    <th className="pb-4">Type</th>
                    <th className="pb-4">Status</th>
                    <th className="pb-4">Fraud Score</th>

                  </tr>

                </thead>

                <tbody>

                  <tr className="border-b border-gray-100">

                    <td className="py-5">
                      Aadhaar_Card.pdf
                    </td>

                    <td className="py-5">
                      PDF
                    </td>

                    <td className="py-5">
                      <span className="bg-green-100 text-green-600 px-4 py-2 rounded-xl text-sm">
                        Verified
                      </span>
                    </td>

                    <td className="py-5">
                      2%
                    </td>

                  </tr>

                  <tr className="border-b border-gray-100">

                    <td className="py-5">
                      Degree_Certificate.pdf
                    </td>

                    <td className="py-5">
                      PDF
                    </td>

                    <td className="py-5">
                      <span className="bg-yellow-100 text-yellow-600 px-4 py-2 rounded-xl text-sm">
                        Suspicious
                      </span>
                    </td>

                    <td className="py-5">
                      68%
                    </td>

                  </tr>

                  <tr>

                    <td className="py-5">
                      Passport.png
                    </td>

                    <td className="py-5">
                      Image
                    </td>

                    <td className="py-5">
                      <span className="bg-green-100 text-green-600 px-4 py-2 rounded-xl text-sm">
                        Verified
                      </span>
                    </td>

                    <td className="py-5">
                      1%
                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </div>

      </div>

    </div>
  )
}