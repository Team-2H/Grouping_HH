import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="min-h-screen bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-400 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-xl text-center">
        <h1 className="text-4xl font-bold text-indigo-600 mb-4">Tailwind 작동 확인 ✅</h1>
        <p className="text-gray-700 text-lg">이 페이지는 Tailwind CSS v4로 스타일링되었습니다.</p>
        <button className="mt-6 px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-blue-300 font-semibold rounded transition">
          버튼 테스트
        </button>
      </div>
    </div>

      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
