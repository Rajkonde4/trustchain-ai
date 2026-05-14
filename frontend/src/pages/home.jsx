import { Link } from "react-router-dom"
import Navbar from "../components/Navbar"

export default function Home() {

  const token = localStorage.getItem(
    "token"
  )

  return (

    <div className="min-h-screen bg-[#F5F7FB] text-[#111827]">

      <Navbar />

      {/* HERO SECTION */}
      <section className="max-w-7xl mx-auto px-6 pt-28 pb-24 text-center">

        <p className="text-[#3B82F6] font-semibold uppercase tracking-[0.2em] text-sm">
          AI-Powered Verification Platform
        </p>

        <h1 className="text-6xl md:text-7xl font-bold mt-8 leading-tight">

          Verify Documents
          <br />
          With AI Precision

        </h1>

        <p className="text-gray-500 text-xl mt-8 max-w-3xl mx-auto leading-relaxed">

          Detect tampering, analyze metadata,
          verify authenticity, generate fraud reports,
          and securely validate documents using AI.

        </p>

        {/* CTA BUTTONS */}
        <div className="flex flex-col md:flex-row gap-6 justify-center mt-12">

          {

            token ? (

              <>

                <Link
                  to="/upload"
                  className="bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-8 py-4 rounded-2xl font-medium shadow-lg"
                >

                  Upload Document

                </Link>

                <Link
                  to="/dashboard"
                  className="bg-white border border-gray-200 px-8 py-4 rounded-2xl font-medium shadow-sm hover:bg-gray-50 transition"
                >

                  View Dashboard

                </Link>

              </>

            ) : (

              <>

                <Link
                  to="/login"
                  className="bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-8 py-4 rounded-2xl font-medium shadow-lg"
                >

                  Login

                </Link>

                <Link
                  to="/signup"
                  className="bg-white border border-gray-200 px-8 py-4 rounded-2xl font-medium shadow-sm hover:bg-gray-50 transition"
                >

                  Create Account

                </Link>

              </>

            )
          }

        </div>

      </section>

      {/* FEATURES */}
      <section className="max-w-6xl mx-auto px-6 pb-24">

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100">

            <h3 className="text-2xl font-bold text-[#111827]">
              OCR Extraction
            </h3>

            <p className="text-gray-500 mt-4 leading-relaxed">

              Extract text from scanned images,
              documents, and PDFs using intelligent OCR analysis.

            </p>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100">

            <h3 className="text-2xl font-bold text-[#111827]">
              Fraud Detection
            </h3>

            <p className="text-gray-500 mt-4 leading-relaxed">

              Detect suspicious metadata,
              tampering indicators,
              and authenticity risks instantly.

            </p>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100">

            <h3 className="text-2xl font-bold text-[#111827]">
              Verification Reports
            </h3>

            <p className="text-gray-500 mt-4 leading-relaxed">

              Generate secure AI-powered verification reports
              with QR-based public validation.

            </p>

          </div>

        </div>

      </section>

      {/* STATS */}
      <section className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-6 pb-24">

        <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 text-center">

          <h2 className="text-4xl font-bold text-[#3B82F6]">
            99%
          </h2>

          <p className="text-gray-500 mt-2">
            Detection Accuracy
          </p>

        </div>

        <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 text-center">

          <h2 className="text-4xl font-bold text-[#3B82F6]">
            OCR
          </h2>

          <p className="text-gray-500 mt-2">
            AI Text Extraction
          </p>

        </div>

        <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 text-center">

          <h2 className="text-4xl font-bold text-[#3B82F6]">
            AI
          </h2>

          <p className="text-gray-500 mt-2">
            Fraud Detection
          </p>

        </div>

        <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 text-center">

          <h2 className="text-4xl font-bold text-[#3B82F6]">
            24/7
          </h2>

          <p className="text-gray-500 mt-2">
            Secure Verification
          </p>

        </div>

      </section>

    </div>
  )
}