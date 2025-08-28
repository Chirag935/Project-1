import { format, formatDistanceToNow } from 'date-fns'

export const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'No data'
  try {
    return format(new Date(timestamp), 'PPp')
  } catch {
    return 'Invalid timestamp'
  }
}

export const formatTimeAgo = (timestamp) => {
  if (!timestamp) return 'Unknown'
  try {
    return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
  } catch {
    return 'Invalid timestamp'
  }
}

export const formatCoordinates = (lat, lng) => {
  return `${lat.toFixed(4)}, ${lng.toFixed(4)}`
}

export const formatPercentage = (value) => {
  if (value === null || value === undefined) return 'N/A'
  return `${Math.round(value)}%`
}

export const formatScore = (score) => {
  if (score === null || score === undefined) return 'N/A'
  return `${Math.round(score)}/100`
}

export const getComfortLevelInfo = (score) => {
  if (score >= 80) return { 
    label: 'Excellent', 
    color: 'text-green-600', 
    bg: 'bg-green-100',
    description: 'Perfect outdoor conditions'
  }
  if (score >= 65) return { 
    label: 'Good', 
    color: 'text-green-500', 
    bg: 'bg-green-100',
    description: 'Great for outdoor activities'
  }
  if (score >= 45) return { 
    label: 'Moderate', 
    color: 'text-yellow-600', 
    bg: 'bg-yellow-100',
    description: 'Acceptable outdoor conditions'
  }
  if (score >= 25) return { 
    label: 'Poor', 
    color: 'text-orange-600', 
    bg: 'bg-orange-100',
    description: 'Less than ideal conditions'
  }
  return { 
    label: 'Very Poor', 
    color: 'text-red-600', 
    bg: 'bg-red-100',
    description: 'Challenging outdoor conditions'
  }
}

export const getWeatherEmoji = (condition) => {
  const weatherEmojis = {
    clear: '☀️',
    partly_cloudy: '⛅',
    overcast: '☁️',
    variable: '🌤️'
  }
  return weatherEmojis[condition] || '🌤️'
}