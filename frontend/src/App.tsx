import React from 'react';

function App() {
  return (
    <div className="flex flex-col min-h-screen font-sans">
      {/* 🟦 네비게이션 바 */}
      <header className="bg-gray-800 text-white p-4 w-[300px]">Nav Bar</header>

      {/* 🟨 콘텐츠 영역 */}
      <main className="flex-1 p-8">
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
          <div className="bg-gray-100 p-4 rounded shadow">카드 1</div>
          <div className="bg-gray-100 p-4 rounded shadow">카드 2</div>
          <div className="bg-gray-100 p-4 rounded shadow">카드 3</div>
        </div>
      </main>

      {/* 🟩 푸터 */}
      <footer className="bg-gray-200 p-4 text-center">Footer</footer>
    </div>
  );
}

export default App;
