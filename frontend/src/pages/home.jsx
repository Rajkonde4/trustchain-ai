import Navbar from "../components/Navbar"

export default function Home() {
  return (
    <div className="bg-black text-white min-h-screen">

      <Navbar />

      <div className="flex flex-col items-center justify-center text-center pt-32">

        <h1 className="text-7xl font-bold text-blue-500">
          TrustChain AI
        </h1>

        <p className="text-gray-400 mt-6 text-xl max-w-2xl">
          AI-Powered Intelligent Document Verification & Fraud Detection Platform
        </p>

        <button className="mt-8 px-8 py-3 bg-blue-600 rounded-xl hover:bg-blue-700 transition">
          Upload Document
        </button>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-12 mt-32">

  <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800">
    <h2 className="text-2xl font-bold text-blue-400">
      OCR Verification
    </h2>

    <p className="text-gray-400 mt-4">
      Extract and analyze text from uploaded documents using AI OCR technology.
    </p>
  </div>

  <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800">
    <h2 className="text-2xl font-bold text-blue-400">
      Fraud Detection
    </h2>

    <p className="text-gray-400 mt-4">
      Detect tampered certificates, fake edits, and suspicious metadata instantly.
    </p>
  </div>

  <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800">
    <h2 className="text-2xl font-bold text-blue-400">
      AI Analytics
    </h2>

    <p className="text-gray-400 mt-4">
      Generate intelligent fraud scores and detailed verification reports.
    </p>
  </div>

</div>
<div className="mt-32 text-center pb-20">

  <h2 className="text-4xl font-bold text-blue-500">
    How It Works
  </h2>

  <div className="flex flex-col md:flex-row justify-center gap-10 mt-12">

    <div className="bg-gray-900 p-6 rounded-xl w-60">
      Upload Document
    </div>

    <div className="bg-gray-900 p-6 rounded-xl w-60">
      AI Verification
    </div>

    <div className="bg-gray-900 p-6 rounded-xl w-60">
      Fraud Analysis
    </div>

    <div className="bg-gray-900 p-6 rounded-xl w-60">
      Generate Report
    </div>

  </div>

</div>

      </div>

    </div>
  )
}