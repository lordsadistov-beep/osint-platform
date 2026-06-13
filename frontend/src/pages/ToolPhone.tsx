import { ToolWidget } from '../components/ToolWidget'

export function ToolPhone() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Phone Checker</h1>
      <p className="mb-4 text-sm text-gray-500">Проверка номера телефона по открытым источникам</p>
      <ToolWidget toolSlug="phone" />
    </div>
  )
}
