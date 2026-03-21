import {
  dayAheadPriceResponseSchema,
  summaryResponseSchema,
  modelListResponseSchema,
  type SummaryResponse,
  type HourlyData,
  type ModelListResponse,
} from './schemas'

const BASE_URL = import.meta.env.PROD
  ? 'https://energy-predictor.appspot.com'
  : ''

function formatDate(date: Date): string {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}${m}${d}`
}

export async function fetchDayAheadPrices(date: Date): Promise<HourlyData> {
  const dateStr = formatDate(date)
  const res = await fetch(`${BASE_URL}/v1/daprices/${dateStr}`)
  const json = await res.json()
  const parsed = dayAheadPriceResponseSchema.parse(json)

  if ('err' in parsed) {
    throw new Error(parsed.err)
  }

  const prices = parsed['Day Ahead Price']
  return Object.keys(prices)
    .sort((a, b) => Number(a) - Number(b))
    .map((key) => prices[key])
}

export async function fetchSummary(
  period: string = 'daily',
  condition: string = 'all',
): Promise<SummaryResponse> {
  const res = await fetch(`${BASE_URL}/v1/summary/${period}/${condition}`)
  const json = await res.json()
  return summaryResponseSchema.parse(json)
}

export async function fetchModelList(): Promise<ModelListResponse> {
  const res = await fetch(`${BASE_URL}/v1/model/list`)
  const json = await res.json()
  return modelListResponseSchema.parse(json)
}
