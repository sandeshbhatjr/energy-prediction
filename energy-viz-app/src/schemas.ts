import { z } from 'zod'

const hourlyDataSchema = z.record(z.string(), z.number())

export const dayAheadPriceResponseSchema = z.object({
  'Day Ahead Price': hourlyDataSchema,
}).or(z.object({
  err: z.string(),
}))

export const summaryResponseSchema = z.object({
  mean: hourlyDataSchema,
  min: hourlyDataSchema,
  max: hourlyDataSchema,
  lq: hourlyDataSchema,
  uq: hourlyDataSchema,
})

export const modelInfoSchema = z.object({
  descr: z.string(),
  acc: z.string(),
})

export const modelListResponseSchema = z.record(z.string(), modelInfoSchema)

export type DayAheadPriceResponse = z.infer<typeof dayAheadPriceResponseSchema>
export type SummaryResponse = z.infer<typeof summaryResponseSchema>
export type ModelListResponse = z.infer<typeof modelListResponseSchema>

export type HourlyData = number[]
export type QuartileData = [number, number][]
