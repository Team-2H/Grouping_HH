import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  const handleButtonClick = async () => {
    try {
      const response = await fetch('http://localhost:5000/grouping');
      const data = await response.json();
      console.log('서버 응답:', data);
      setMessage(data.message); // 📥 응답 데이터 저장
    } catch (error) {
      console.error('서버 호출 실패:', error);
    }
  };

  return (
    <div className="flex flex-col min-h-screen font-sans">
      {/* 🟦 네비게이션 바 */}
      <header className="bg-gray-800 text-white p-4">Nav Bar</header>

      {/* 🟨 콘텐츠 영역 */}
      <main className="flex-1 p-8">
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
          <div className="bg-gray-100 p-4 rounded shadow">카드 1</div>
          <div className="bg-gray-100 p-4 rounded shadow">카드 2</div>
          <div className="bg-gray-100 p-4 rounded shadow">카드 3</div>
        </div>
      </main>

      {/* 🟦 서버 응답 카드 */}
      {message && (
        <div className="bg-white p-4 border rounded shadow mt-8">
          <h3 className="font-semibold mb-2">서버 응답</h3>
          <p>{message}</p>
        </div>
      )}

      {/* 🔵 버튼 추가 */}
      <div className="mt-12 mb-10 flex justify-center">
        <button
          onClick={handleButtonClick}
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          서버 호출
        </button>
      </div>

      {/* 🟩 푸터 */}
      <footer className="bg-gray-200 p-4 text-center">Footer</footer>
    </div>
  );
}

export default App;
