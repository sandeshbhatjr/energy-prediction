import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import './toolbar.css'

interface ToolbarProps {
  selectedDate: Date
  onDateChange: (date: Date) => void
}

const MIN_DATE = new Date(2015, 0, 1)

export default function Toolbar({ selectedDate, onDateChange }: ToolbarProps) {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)

  return (
    <div id="tool-bar">
      <div id="custom-date-picker" className="custom-date-picker-class">
        <DatePicker
          minDate={MIN_DATE}
          maxDate={tomorrow}
          autoFocus
          selected={selectedDate}
          onChange={(date) => date && onDateChange(date)}
          inline
        />
      </div>
    </div>
  )
}
