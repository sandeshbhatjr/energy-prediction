import { useQuery } from '@tanstack/react-query'
import { fetchDayAheadPrices, fetchSummary, fetchModelList } from './api'
import type { HourlyData, QuartileData, SummaryResponse } from './schemas'

export function useDayAheadPrices(date: Date) {
  return useQuery({
    queryKey: ['daprices', date.toISOString().slice(0, 10)],
    queryFn: () => fetchDayAheadPrices(date),
  })
}

export function useSummary(period = 'daily', condition = 'all') {
  return useQuery({
    queryKey: ['summary', period, condition],
    queryFn: () => fetchSummary(period, condition),
    select: (data: SummaryResponse): {
      mean: HourlyData
      quartiles: QuartileData
      min: number
      max: number
    } => {
      const mean = Object.keys(data.mean)
        .sort((a, b) => Number(a) - Number(b))
        .map((k) => data.mean[k])
      const lq = Object.keys(data.lq)
        .sort((a, b) => Number(a) - Number(b))
        .map((k) => data.lq[k])
      const uq = Object.keys(data.uq)
        .sort((a, b) => Number(a) - Number(b))
        .map((k) => data.uq[k])
      const quartiles: QuartileData = lq.map((l, i) => [l, uq[i]])
      const minVal = Math.min(
        ...Object.keys(data.min).map((k) => data.min[k]),
      )
      const maxVal = Math.max(
        ...Object.keys(data.max).map((k) => data.max[k]),
      )
      return { mean, quartiles, min: minVal, max: maxVal }
    },
  })
}

export function useModelList() {
  return useQuery({
    queryKey: ['models'],
    queryFn: fetchModelList,
  })
}
