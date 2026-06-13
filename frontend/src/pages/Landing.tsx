import { Link, useNavigate } from 'react-router-dom'
import { Button } from '../components/common/Button'
import { Card } from '../components/common/Card'

export function Landing() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center">
      <section className="flex min-h-[80vh] flex-col items-center justify-center px-4 text-center">
        <h1 className="text-5xl font-bold text-gray-100">
          OSINT <span className="text-primary-400">Platform</span>
        </h1>
        <p className="mt-4 max-w-xl text-lg text-gray-400">
          Учись методикам OSINT и сразу применяй их на практике через встроенные инструменты.
        </p>
        <div className="mt-8 flex gap-4">
          <Button size="lg" onClick={() => navigate('/register')}>
            Начать обучение
          </Button>
          <Button size="lg" variant="secondary" onClick={() => navigate('/login')}>
            Войти
          </Button>
        </div>
      </section>

      <section className="w-full max-w-5xl px-4 py-16">
        <h2 className="mb-8 text-center text-2xl font-semibold text-gray-200">Возможности</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {[
            { title: '📚 Уроки', desc: 'Структурированные материалы по OSINT методикам' },
            { title: '🔍 Инструменты', desc: 'Username, email, domain, phone поиск' },
            { title: '🏆 Челленджи', desc: 'CTF-задания для закрепления навыков' },
            { title: '🔗 Граф связей', desc: 'Визуализация связей между данными' },
          ].map((f) => (
            <Card key={f.title} className="text-center">
              <div className="text-3xl">{f.title.split(' ')[0]}</div>
              <h3 className="mt-2 font-semibold">{f.title}</h3>
              <p className="mt-1 text-sm text-gray-500">{f.desc}</p>
            </Card>
          ))}
        </div>
      </section>

      <section className="w-full max-w-3xl px-4 py-16">
        <h2 className="mb-8 text-center text-2xl font-semibold text-gray-200">Как это работает</h2>
        <div className="grid gap-6 md:grid-cols-3">
          {[
            { step: '1', title: 'Выбери урок', desc: 'Изучи теорию по OSINT методике' },
            { step: '2', title: 'Изучи теорию', desc: 'Разбери реальные примеры' },
            { step: '3', title: 'Примени на практике', desc: 'Используй встроенный инструмент прямо на странице урока' },
          ].map((s) => (
            <div key={s.step} className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary-600 text-xl font-bold">
                {s.step}
              </div>
              <h3 className="mt-3 font-semibold text-gray-200">{s.title}</h3>
              <p className="mt-1 text-sm text-gray-500">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
