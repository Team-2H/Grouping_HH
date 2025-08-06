import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState([]); // 초기값을 빈 배열로
  const [groupCount, setGroupCount] = useState('');
  const [maxFactor, setMaxFactor] = useState('');
  const [minFactor, setMinFactor] = useState('');
  // const [userData, setUserData] = useState([...]);
  // const [userData, setUserData] = useState(() =>
  //   Array.from({ length: 5 }, (_, i) => ({
  //     name: `회원${i + 1}`,
  //     age: '',
  //     height: '',
  //     weight: '',
  //     muscle_mass: '',
  //     experience: '',
  //     gender: 0,
  //   }))
  // );
  const [customColumns, setCustomColumns] = useState([
    '컬럼1',
    '컬럼2',
    '컬럼3',
  ]); // 사용자 정의 컬럼명
  const [userData, setUserData] = useState([
    { name: '회원1', values: ['', '', ''] },
    { name: '회원2', values: ['', '', ''] },
    { name: '회원3', values: ['', '', ''] },
    { name: '회원4', values: ['', '', ''] },
    { name: '회원5', values: ['', '', ''] },
  ]);

  /* 컬럼명 변경 핸들러 */
  const handleColumnNameChange = (colIdx: number, value: string) => {
    const newCols = [...customColumns];
    newCols[colIdx] = value;
    setCustomColumns(newCols);
  };

  // const handleUserInputChange = (
  //   index: number,
  //   field: string,
  //   value: string
  // ) => {
  //   const newData = [...userData];
  //   newData[index][field] = value;
  //   setUserData(newData);
  // };

  const handleNameChange = (rowIdx: number, value: string) => {
    const newData = [...userData];
    newData[rowIdx].name = value;
    setUserData(newData);
  };

  const handleValueChange = (rowIdx: number, colIdx: number, value: string) => {
    const newData = [...userData];
    newData[rowIdx].values[colIdx] = value;
    setUserData(newData);
  };

  const addUserRow = () => {
    setUserData([
      ...userData,
      {
        name: `회원${userData.length + 1}`,
        values: Array(customColumns.length).fill(''),
      },
    ]);
  };

  const addColumn = () => {
    setCustomColumns([...customColumns, `컬럼${customColumns.length + 1}`]);
    setUserData(
      userData.map((user) => ({
        ...user,
        values: [...user.values, ''],
      }))
    );
  };

  const handleButtonClick = async () => {
    const processedUserData = userData.map((user) => {
      const result: Record<string, any> = { name: user.name };
      user.values.forEach((val, idx) => {
        const key = `column${String(idx + 1).padStart(2, '0')}`; // column01, column02, ...
        result[key] = Number(val); // 숫자 변환도 여기서 같이 처리
      });
      return result;
    });

    try {
      const response = await fetch('http://127.0.0.1:5000/grouping', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          groupCount: Number(groupCount),
          maxFactor: Number(maxFactor),
          minFactor: Number(minFactor),
          userData: processedUserData,
        }),
      });
      const data = await response.json();
      setMessage(data.labels);
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
        {/* 🟦 서버 응답 카드 */}
        {message.length > 0 && (
          <div className="bg-white p-4 border rounded shadow mt-8">
            <h3 className="font-semibold mb-4 text-lg">
              서버 응답 (클러스터 결과)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {message.map((item, idx) => (
                <div key={idx} className="p-4 border rounded shadow bg-blue-50">
                  <p className="font-semibold">🧑 {item.name}</p>
                  <p className="text-sm text-gray-600">
                    📦 Cluster {item.cluster}
                  </p>
                </div>
              ))}
            </div>
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
                {customColumns.map((col, colIdx) => (
                  <th key={colIdx} className="border px-2 py-1">
                    <input
                      value={col}
                      onChange={(e) =>
                        handleColumnNameChange(colIdx, e.target.value)
                      }
                      className="w-full border rounded px-1 py-0.5"
                    />
                  </th>
                ))}
                <th className="border px-2 py-1">
                  <button
                    onClick={addColumn}
                    className="text-blue-600 hover:underline"
                  >
                    + 열 추가
                  </button>
                </th>
              </tr>
            </thead>

            <tbody>
              {userData.map((user, rowIdx) => (
                <tr key={rowIdx} className="odd:bg-white even:bg-gray-50">
                  <td className="border px-2 py-1">
                    <input
                      value={user.name}
                      onChange={(e) => handleNameChange(rowIdx, e.target.value)}
                      className="w-full border rounded px-1 py-0.5"
                    />
                  </td>
                  {user.values.map((val, colIdx) => (
                    <td key={colIdx} className="border px-2 py-1">
                      <input
                        value={val}
                        onChange={(e) =>
                          handleValueChange(rowIdx, colIdx, e.target.value)
                        }
                        className="w-full border rounded px-1 py-0.5"
                      />
                    </td>
                  ))}
                  <td className="border px-2 py-1" />
                </tr>
              ))}
              <tr>
                <td
                  colSpan={customColumns.length + 2}
                  className="text-center py-2"
                >
                  <button
                    onClick={addUserRow}
                    className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    + 행 추가
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
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
      </main>

      {/* 🟩 푸터 */}
      <footer className="bg-gray-200 p-4 text-center">Footer</footer>
    </div>
  );
}

export default App;
