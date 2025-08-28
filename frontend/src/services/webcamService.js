import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

class WebcamService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000
    })
  }

  async getAllWebcams() {
    try {
      const response = await this.api.get('/api/webcams')
      return response.data
    } catch (error) {
      console.error('Failed to fetch webcams:', error)
      throw error
    }
  }

  async getLatestAnalysis(webcamId) {
    try {
      const response = await this.api.get(`/api/webcams/${webcamId}/latest`)
      return response.data
    } catch (error) {
      console.error(`Failed to fetch latest analysis for ${webcamId}:`, error)
      throw error
    }
  }

  async getAllLatest() {
    try {
      const response = await this.api.get('/api/all-latest')
      return response.data
    } catch (error) {
      console.error('Failed to fetch all latest data:', error)
      throw error
    }
  }

  async checkHealth() {
    try {
      const response = await this.api.get('/')
      return response.data
    } catch (error) {
      console.error('Health check failed:', error)
      throw error
    }
  }
}

export const webcamService = new WebcamService()