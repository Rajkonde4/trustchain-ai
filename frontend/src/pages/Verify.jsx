import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

export default function Verify() {

  const { id } = useParams()

  const [report, setReport] = useState(null)

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/verify/${id}`)

      .then((res) => res.json())

      .then((data) => {

        console.log(data)

        setReport(data)

      })

  }, [id])

  if (!report) {

    return (

      <div className="min-h-screen flex items-center justify-center text-2xl font-bold">

        Loading Verification...

      </div>

    )

  }

  return (

    <div className="min-h-screen bg-[#F5F7FB] flex items-center justify-center p-10">

      <div className="bg-white rounded-3xl shadow-xl p-10 w-full max-w-2xl border border-gray-200">

        <div className="text-center">

          <h1 className="text-5xl font-bold text-[#3B82F6]">
            TrustChain AI
          </h1>

          <p className="mt-4 text-gray-500 text-lg">
            Public Verification Portal
          </p>

        </div>

        <div className="mt-10 text-center">

          <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-green-100">

            <span className="text-5xl">
              ✅
            </span>

          </div>

          <h2 className="text-3xl font-bold mt-6">
            Document Verified
          </h2>

          <p className="text-gray-500 mt-3">
            This document exists in TrustChain AI verification records.
          </p>

        </div>

        <div className="mt-12 space-y-6">

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

            <h3 className="text-2xl font-bold mt-2">
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

          <div className="bg-gray-50 rounded-2xl p-6 break-all">

            <p className="text-gray-500 text-sm">
              Document Hash
            </p>

            <h3 className="text-sm font-medium mt-2">
              {report.document_hash}
            </h3>

          </div>

        </div>

      </div>

    </div>
  )
}