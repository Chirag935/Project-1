import React from 'react'
import WebcamCard from './WebcamCard'
import WebcamDetails from './WebcamDetails'

const Dashboard = ({ webcamData, selectedWebcam, onWebcamSelect, onCloseDetails }) => {
  if (selectedWebcam) {
    return (
      <div className="h-full">
        <WebcamDetails 
          webcam={selectedWebcam} 
          onClose={onCloseDetails}
        />
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b bg-gray-50">
        <h2 className="text-xl font-bold text-gray-800">Live Webcam Feed</h2>
        <p className="text-sm text-gray-600 mt-1">
          Real-time micro-climate monitoring from {webcamData.length} locations
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {webcamData.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-400 text-4xl mb-4">📹</div>
            <p className="text-gray-500">No webcam data available</p>
            <p className="text-sm text-gray-400 mt-2">
              Waiting for real-time updates...
            </p>
          </div>
        ) : (
          webcamData.map((webcam) => (
            <WebcamCard
              key={webcam.webcam_id}
              webcam={webcam}
              onClick={() => onWebcamSelect(webcam)}
            />
          ))
        )}
      </div>

      <div className="p-4 border-t bg-gray-50">
        <div className="text-xs text-gray-500 space-y-1">
          <div className="flex justify-between">
            <span>Total Locations:</span>
            <span className="font-medium">{webcamData.length}</span>
          </div>
          <div className="flex justify-between">
            <span>Active Monitoring:</span>
            <span className="font-medium text-green-600">
              {webcamData.filter(w => w.status === 'success').length}
            </span>
          </div>
          <div className="flex justify-between">
            <span>Data Sources:</span>
            <span className="font-medium">Public Webcams</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard