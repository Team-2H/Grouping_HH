import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [groupCount, setGroupCount] = useState('');
  const [maxFactor, setMaxFactor] = useState('');
  const [minFactor, setMinFactor] = useState('');
  const [userData, setUserData] = useState(() =>
    Array.from({ length: 5 }, (_, i) => ({
      name: `회원${i + 1}`,
      age: '',
      height: '',
      weight: '',
      muscle_mass: '',
      experience: '',
      gender: 0,
    }))
  );

  const handleUserInputChange = (
    index: number,
    field: string,
    value: string
  ) => {
    const newData = [...userData];
    newData[index][field] = value;
    setUserData(newData);
  };

  const addUserRow = () => {
    setUserData([
      ...userData,
      {
        name: `회원${userData.length + 1}`,
        age: '',
        height: '',
        weight: '',
        muscle_mass: '',
        experience: '',
        gender: 0,
      },
    ]);
  };
  const handleButtonClick = async () => {
    try {
      const response = await fetch('http://localhost:5000/grouping', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // 이게 없으면 415 오류!
        },
        body: JSON.stringify({
          groupCount: Number(groupCount),
          maxFactor: Number(maxFactor),
          minFactor: Number(minFactor),
          userData: userData.map((u) => ({
            ...u,
            age: Number(u.age),
            height: Number(u.height),
            weight: Number(u.weight),
            muscle_mass: Number(u.muscle_mass),
            experience: Number(u.experience),
            gender: Number(u.gender),
          })),
        }),
      });
      const data = await response.json();
      console.log('서버 응답:', data);
      console.log('서버 응답:', data.labels);

      setMessage(data.lables); // 📥 응답 데이터 저장
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

      {/* input창 */}
      <div className="mt-6 flex flex-col sm:flex-row justify-center gap-4">
        <input
          type="number"
          placeholder="최대 그룹 수 (groupCount)"
          value={groupCount}
          onChange={(e) => setGroupCount(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="number"
          placeholder="maxFactor"
          value={maxFactor}
          onChange={(e) => setMaxFactor(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="number"
          placeholder="minFactor"
          value={minFactor}
          onChange={(e) => setMinFactor(e.target.value)}
          className="border p-2 rounded"
        />
      </div>

      {/* 유저추가 */}
      <div className="mt-6 px-8 overflow-auto">
        <table className="min-w-full border border-gray-300 text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">이름</th>
              <th className="border px-2 py-1">나이</th>
              <th className="border px-2 py-1">키</th>
              <th className="border px-2 py-1">몸무게</th>
              <th className="border px-2 py-1">골격근량</th>
              <th className="border px-2 py-1">경력</th>
              <th className="border px-2 py-1">성별</th>
            </tr>
          </thead>
          <tbody>
            {userData.map((user, idx) => (
              <tr key={idx} className="odd:bg-white even:bg-gray-50">
                <td className="border px-2 py-1">
                  <input
                    type="text"
                    value={user.name}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'name', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  />
                </td>
                <td className="border px-2 py-1">
                  <input
                    type="number"
                    value={user.age}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'age', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  />
                </td>
                <td className="border px-2 py-1">
                  <input
                    type="number"
                    value={user.height}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'height', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  />
                </td>
                <td className="border px-2 py-1">
                  <input
                    type="number"
                    value={user.weight}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'weight', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  />
                </td>
                <td className="border px-2 py-1">
                  <input
                    type="number"
                    value={user.muscle_mass}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'muscle_mass', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  />
                </td>
                <td className="border px-2 py-1">
                  <input
                    type="number"
                    value={user.experience}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'experience', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  />
                </td>
                <td className="border px-2 py-1">
                  <select
                    value={user.gender}
                    onChange={(e) =>
                      handleUserInputChange(idx, 'gender', e.target.value)
                    }
                    className="w-full border rounded px-1 py-0.5"
                  >
                    <option value={0}>남</option>
                    <option value={1}>여</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* + 추가 버튼 */}
        <div className="flex justify-center mt-4">
          <button
            onClick={addUserRow}
            className="px-4 py-1 bg-green-600 text-white rounded hover:bg-green-700"
          >
            + 유저 추가
          </button>
        </div>
      </div>

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
