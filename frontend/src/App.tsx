import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState([]); // 초기값을 빈 배열로
  const [groupCount, setGroupCount] = useState('');
  const [maxFactor, setMaxFactor] = useState('');
  const [minFactor, setMinFactor] = useState('');

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
  // 고정 폭(px) — 네가 쓰는 w-48(≈192px) 기준
  const NAME_COL_PX = 100; // "이름" 열
  const ADD_COL_PX = 100; // "+ 열 추가" 열 (원하는 값으로 조정 가능)

  // 남은 폭을 중간 컬럼 개수로 균등 분배
  const middleColWidth = `calc((100% - ${NAME_COL_PX + ADD_COL_PX}px) / ${customColumns.length || 1})`;

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
  // 컬럼 제거 메서드
  const removeColumn = (colIdx: number) => {
    // 1. 컬럼 배열에서 제거
    const newCols = customColumns.filter((_, idx) => idx !== colIdx);
    setCustomColumns(newCols);

    // 2. 각 유저 데이터 values 배열에서도 같은 인덱스 제거
    const newUserData = userData.map((user) => ({
      ...user,
      values: user.values.filter((_, idx) => idx !== colIdx),
    }));
    setUserData(newUserData);
  };
  // 행 제거 메서드
  const removeUserRow = (rowIdx: number) => {
    const newUserData = userData.filter((_, idx) => idx !== rowIdx);
    setUserData(newUserData);
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

        {/* 유저데이터 table */}
        <div className="mt-6 px-8 overflow-x-auto relative">
          {/* <table className="min-w-full border border-gray-300 text-sm"> */}
          <table className="w-full table-auto border border-gray-300 text-sm border-separate border-spacing-0">
            <colgroup>
              {/* 1) 이름 열: 고정 폭 */}
              <col style={{ width: NAME_COL_PX }} />
              {/* 2) 중간 컬럼들: 남은 폭을 균등 분배 */}
              {customColumns.map((_, i) => (
                <col key={i} style={{ width: middleColWidth }} />
              ))}
              {/* 3) "+ 열 추가" 열: 고정 폭 */}
              <col style={{ width: ADD_COL_PX }} />
            </colgroup>
            <thead className="bg-gray-100 sticky top-0 z-20">
              <tr>
                <th
                  // className="border px-2 py-1 sticky left-0 top-0 z-40 bg-gray-100 w-40 md:w-48"
                  className="border px-2 py-1 sticky left-0 top-0 z-40 bg-gray-100"
                  style={{ minWidth: '10rem' }}
                >
                  이름
                </th>
                {customColumns.map((col, colIdx) => (
                  <th key={colIdx} className="border px-2 py-1 w-15 md:w-32">
                    <div className="flex items-center gap-2">
                      <input
                        value={col}
                        onChange={(e) =>
                          handleColumnNameChange(colIdx, e.target.value)
                        }
                        className="flex-1 min-w-0 border rounded px-1 py-0.5 text-xs"
                      />
                      <button
                        onClick={() => removeColumn(colIdx)}
                        className="shrink-0 text-red-500 hover:text-red-700 px-1"
                        aria-label={`컬럼 ${colIdx + 1} 삭제`}
                        title="열 삭제"
                      >
                        ✕
                      </button>
                    </div>
                  </th>
                ))}
                <th className="border px-2 py-1 whitespace-nowrap">
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
                  <td className="border px-2 py-1 sticky left-0 z-10 bg-white">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => removeUserRow(rowIdx)}
                        className="shrink-0 text-red-500 hover:text-red-700 px-1"
                        aria-label={`행 ${rowIdx + 1} 삭제`}
                        title="행 삭제"
                        type="button"
                      >
                        ✕
                      </button>
                      <input
                        value={user.name}
                        onChange={(e) =>
                          handleNameChange(rowIdx, e.target.value)
                        }
                        className="w-full border rounded px-1 py-0.5"
                      />
                    </div>
                  </td>
                  {user.values.map((val, colIdx) => (
                    <td
                      key={colIdx}
                      className="border px-2 py-1 w-24 sm:w-28 md:w-32"
                    >
                      <input
                        value={val}
                        onChange={(e) =>
                          handleValueChange(rowIdx, colIdx, e.target.value)
                        }
                        className="w-full min-w-0 border rounded px-1 py-0.5 text-xs"
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

        {/* 🔵 submit 버튼 */}
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
