import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

export default function Verify() {

  const { id } = useParams()

  const [report, setReport] = useState(null)

  const [loading, setLoading] = useState(true)

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/verify/${id}`)

      .then((res) => res.json())

      .then((data) => {

        console.log(data)

        setReport(data)

        setLoading(false)

      })

      .catch((error) => {

        console.log(error)

        setLoading(false)
      })

  }, [id])

  // LOADING
  if (loading) {

    return (

      <div className="min-h-screen flex items-center justify-center bg-[#F5F7FB]">

        <h1 className="text-3xl font-bold">
          Loading Verification...
        </h1>

      </div>

    )
  }

  // INVALID REPORT
  if (!report || report.message) {

    return (

      <div className="min-h-screen flex items-center justify-center bg-[#F5F7FB] p-10">

        <div className="bg-white rounded-3xl shadow-xl p-10 max-w-xl w-full text-center border border-gray-200">

          <div className="w-24 h-24 rounded-full bg-red-100 flex items-center justify-center mx-auto">

            <span className="text-5xl">
              ❌
            </span>

          </div>

          <h1 className="text-4xl font-bold mt-8">
            Verification Failed
          </h1>

          <p className="text-gray-500 mt-4 text-lg">
            This document does not exist in TrustChain AI records.
          </p>

        </div>

      </div>

    )
  }

  // RISK COLORS
  const riskStyles = {

    Low: {
      bg: "bg-green-100",
      text: "text-green-600",
      icon: "✅",
      title: "Document Verified"
    },

    Medium: {
      bg: "bg-yellow-100",
      text: "text-yellow-600",
      icon: "⚠️",
      title: "Medium Risk Document"
    },

    High: {
      bg: "bg-red-100",
      text: "text-red-600",
      icon: "❌",
      title: "High Risk Document"
    }

  }

  const currentRisk =
    riskStyles[report.fraud_risk] || riskStyles.Low

  return (

    <div className="min-h-screen bg-[#F5F7FB] flex items-center justify-center p-10">

      <div className="bg-white rounded-3xl shadow-2xl p-10 w-full max-w-3xl border border-gray-200">

        {/* HEADER */}
        <div className="text-center">

          <h1 className="text-5xl font-bold text-[#3B82F6]">
            TrustChain AI
          </h1>

          <p className="mt-4 text-gray-500 text-lg">
            Public Verification Portal
          </p>

        </div>

        {/* STATUS */}
        <div className="mt-12 text-center">

          <div className={`inline-flex items-center justify-center w-28 h-28 rounded-full ${currentRisk.bg}`}>

            <span className="text-6xl">
              {currentRisk.icon}
            </span>

          </div>

          <h2 className={`text-4xl font-bold mt-8 ${currentRisk.text}`}>

            {currentRisk.title}

          </h2>

          <p className="text-gray-500 mt-4 text-lg">

            This verification result was generated securely
            through TrustChain AI.

          </p>

        </div>

        {/* DETAILS */}
        <div className="mt-14 grid grid-cols-1 md:grid-cols-2 gap-6">

          <div className="bg-gray-50 rounded-2xl p-6">

            <p className="text-gray-500 text-sm">
              Verification Status
            </p>

            <h3 className="text-2xl font-bold mt-2">
              {report.verification_status}
            </h3>

          </div>

          <div className="bg-gray-50 rounded-2xl p-6">

            <p className="text-gray-500 text-sm">
              Document Category
            </p>

            <h3 className="text-2xl font-bold mt-2">
              {report.document_category}
            </h3>

          </div>

          <div className="bg-gray-50 rounded-2xl p-6">

            <p className="text-gray-500 text-sm">
              Fraud Risk
            </p>

            <h3 className={`text-2xl font-bold mt-2 ${currentRisk.text}`}>

              {report.fraud_risk}

            </h3>

          </div>

          <div className="bg-gray-50 rounded-2xl p-6">

            <p className="text-gray-500 text-sm">
              Confidence Score
            </p>

            <h3 className="text-2xl font-bold mt-2">

              {report.confidence_score}%

            </h3>

          </div>

        </div>

        {/* HASH */}
        <div className="mt-10 bg-gray-50 rounded-2xl p-6 break-all">

          <p className="text-gray-500 text-sm">
            Document Hash
          </p>

          <h3 className="text-sm font-medium mt-3">
            {report.document_hash}
          </h3>

        </div>

        {/* FOOTER */}
        <div className="mt-12 border-t border-gray-100 pt-8 text-center">

          <p className="text-gray-500">

            Verified securely using AI-powered document
            authentication technology.

          </p>

        </div>

      </div>

    </div>
  )
}