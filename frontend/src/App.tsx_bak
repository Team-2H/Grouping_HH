import React, { useState, useEffect } from 'react';

function App() {
  // ⬆️ import 아래/컴포넌트 위쪽 아무대나
  type Team = { cluster: number; members: string[] };

  const normalizeLabels = (labels: any): Team[] => {
    if (!labels) return [];
    if (typeof labels === 'object' && !Array.isArray(labels)) {
      return Object.keys(labels)
        .sort((a, b) => Number(a) - Number(b))
        .map((k) => ({ cluster: Number(k), members: labels[k] as string[] }));
    }
    // (혹시 배열로 오면 대비)
    if (Array.isArray(labels)) {
      // [[...], [...]] 형태 가정
      return labels.map((members, i) => ({ cluster: i, members }));
    }
    return [];
  };

  // 기존: const [message, setMessage] = useState([]);
  const [message, setMessage] = useState<Team[]>([]);
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

  // ⬇⬇⬇ 추가: 업로드 모드 / 파일 상태 / CSV 엔드포인트
  const [mode, setMode] = useState<'manual' | 'csv'>('manual');
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const CSV_ENDPOINT = 'http://127.0.0.1:5000/groupingByCSV';

  // (상단 state 구역 인근에 추가)
  // ✨ 추가
  const [showWeight, setShowWeight] = useState(false); // 가중치 행 표시/숨김
  const [factorWeight, setFactorWeight] = useState<number[]>(
    Array(customColumns.length).fill(1) // 기본 가중치 1
  );
  // ✨ 추가: 컬럼명을 서버로 보낼 키로 변환(영문 권장: age, height, ...)
  const toKey = (label: string) =>
    label
      .trim()
      .toLowerCase()
      .replace(/[\s\-]+/g, '_') // 공백/하이픈 → _
      .replace(/[^\w]/g, '') // 영문/숫자/언더스코어만
      .replace(/^(\d)/, '_$1'); // 숫자로 시작하면 앞에 _
  // 고정 폭(px) — 네가 쓰는 w-48(≈192px) 기준
  const NAME_COL_PX = 100; // "이름" 열
  const ADD_COL_PX = 100; // "+ 열 추가" 열 (원하는 값으로 조정 가능)

  // 남은 폭을 중간 컬럼 개수로 균등 분배
  const middleColWidth = `calc((100% - ${NAME_COL_PX + ADD_COL_PX}px) / ${customColumns.length || 1})`;

  // ⏳ 로딩 오버레이
  const [isLoading, setIsLoading] = useState(false);
  const MIN_SPINNER_MS = 1000; // 최소 1초

  // 어떤 비동기 작업이든 감싸면, 로딩 오버레이가 최소 1초 유지됨
  const withLoading = async (task: () => Promise<void>) => {
    setIsLoading(true);
    const start = Date.now();
    try {
      await task();
    } finally {
      const elapsed = Date.now() - start;
      const remain = MIN_SPINNER_MS - elapsed;
      if (remain > 0) {
        setTimeout(() => setIsLoading(false), remain);
      } else {
        setIsLoading(false);
      }
    }
  };

  // 오버레이 뜰 때 스크롤 잠그기(선택)
  useEffect(() => {
    document.documentElement.style.overflow = isLoading ? 'hidden' : '';
    return () => {
      document.documentElement.style.overflow = '';
    };
  }, [isLoading]);

  /* 컬럼명 변경 핸들러 */
  const handleColumnNameChange = (colIdx: number, value: string) => {
    const newCols = [...customColumns];
    newCols[colIdx] = value;
    setCustomColumns(newCols);
  };

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
    // ✨ 추가: 가중치도 동기화
    setFactorWeight((prev) => [...prev, 1]);
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
    // ✨ 추가: 가중치도 동일 인덱스 제거
    setFactorWeight((prev) => prev.filter((_, idx) => idx !== colIdx));
  };
  // 행 제거 메서드
  const removeUserRow = (rowIdx: number) => {
    const newUserData = userData.filter((_, idx) => idx !== rowIdx);
    setUserData(newUserData);
  };

  // ...기존 handleButtonClick 바로 위/아래 어느 곳이나
  const handleCsvUpload = async () => {
    if (!csvFile) {
      alert('CSV 파일을 선택해 주세요.');
      return;
    }

    const formData = new FormData();
    // 백엔드가 기대하는 필드명에 맞춰 조정하세요 (보통 'file' or 'csv')
    formData.append('csvData', csvFile, csvFile.name);

    // 숫자 파라미터도 함께 전송 (서버에서 사용한다면)
    if (groupCount) formData.append('groupCount', String(groupCount));
    if (maxFactor) formData.append('maxFactor', String(maxFactor));
    if (minFactor) formData.append('minFactor', String(minFactor));

    try {
      await withLoading(async () => {
        const res = await fetch(CSV_ENDPOINT, {
          method: 'POST',
          body: formData, // ❗️multipart/form-data: Content-Type 수동 지정 금지
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setMessage(normalizeLabels(data.labels));
      });
    } catch (e) {
      console.error('CSV 업로드 실패:', e);
      alert('CSV 업로드 중 오류가 발생했습니다. 콘솔을 확인하세요.');
    }
  };

  const handleButtonClick = async () => {
    // 1) 컬럼명 → 키로 변환 (예: 'muscle mass' → 'muscle_mass')
    const keys = customColumns.map(toKey);

    // 2) 가중치 객체 만들기 (name 제외)
    //    요구사항: factorWeight는 배열이지만 서버에는 [{ key: weight, ... }] 형태로 보냄
    const factorWeightObj: Record<string, number> = {};
    keys.forEach((k, i) => {
      factorWeightObj[k] = Number(factorWeight[i] ?? 1);
    });

    // 3) 유저 데이터 매핑 (각 컬럼 값을 위 keys로 매핑)
    const processedUserData = userData.map((user) => {
      const obj: Record<string, any> = { name: user.name };
      keys.forEach((k, i) => {
        obj[k] = Number(user.values[i]); // 숫자 변환
      });
      return obj;
    });

    // 기본 payload
    const payload: Record<string, any> = {
      groupCount: Number(groupCount),
      maxFactor: Number(maxFactor),
      minFactor: Number(minFactor),
      userData: processedUserData,
    };

    // ✨ 조건부 factorWeight 포함
    if (showWeight) {
      const factorWeightObj: Record<string, number> = {};
      keys.forEach(
        (k, i) => (factorWeightObj[k] = Number(factorWeight[i] ?? 1))
      );

      // 전부 1이면 굳이 안 보냄 (원하면 이 조건을 제거해 항상 보내도 됨)
      const anyNotOne = Object.values(factorWeightObj).some((v) => v !== 1);
      if (anyNotOne) {
        payload.factorWeight = [factorWeightObj];
      }
    }
    // showWeight === false 인 경우는 factorWeight를 아예 안 넣음

    try {
      await withLoading(async () => {
        const res = await fetch('http://127.0.0.1:5000/grouping', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        // 기존: setMessage(data.labels);
        setMessage(normalizeLabels(data.labels));
      });
    } catch (e) {
      console.error('서버 호출 실패:', e);
    }
  };

  return (
    <div className="flex flex-col min-h-screen font-sans">
      {isLoading && (
        <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm">
          <div
            className="w-16 h-16 rounded-full border-4 border-gray-300 border-t-blue-600 animate-spin"
            aria-hidden="true"
          />
          <p className="mt-4 text-gray-800 font-medium">분석 중…</p>
          <p className="text-xs text-gray-500 mt-1">
            잠시만 기다려주세요 (≈1초)
          </p>
        </div>
      )}
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
              {message.map((team) => (
                <div
                  key={team.cluster}
                  className="p-4 border rounded shadow bg-blue-50"
                >
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-semibold">👥 팀 {team.cluster + 1}</p>
                    <span className="text-xs text-gray-600">
                      인원 {team.members.length}명
                    </span>
                  </div>
                  <ul className="space-y-1">
                    {team.members.map((name, i) => (
                      <li
                        key={`${team.cluster}-${i}`}
                        className="flex items-center gap-2"
                      >
                        <span className="inline-block w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span className="text-sm">{name}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
        {/* ✅ 모드 전환 토글 */}
        <div className="mt-4 flex items-center gap-2">
          <button
            type="button"
            onClick={() => setMode('manual')}
            className={`px-3 py-1 rounded border ${mode === 'manual' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            수동 입력
          </button>
          <button
            type="button"
            onClick={() => setMode('csv')}
            className={`px-3 py-1 rounded border ${mode === 'csv' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            CSV 업로드
          </button>
        </div>

        {/* 공통 파라미터 (groupCount/max/min) */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
          {/* groupCount */}
          <div className="flex flex-col">
            <label
              htmlFor="groupCount"
              className="text-sm font-medium text-gray-800"
              title="클러스터링으로 만들 팀의 최대 개수"
            >
              최대 그룹 수 (groupCount)
            </label>
            <input
              id="groupCount"
              type="number"
              min={1}
              placeholder="예: 3"
              value={groupCount}
              onChange={(e) => setGroupCount(e.target.value)}
              className="border p-2 rounded mt-1"
              aria-describedby="groupCountHelp"
            />
            <p id="groupCountHelp" className="mt-1 text-xs text-gray-500">
              만들 팀의 <b>최대 개수</b>를 제한합니다. 비워두면 기본값을
              사용합니다.
            </p>
          </div>

          {/* maxFactor */}
          <div className="flex flex-col">
            <label
              htmlFor="maxFactor"
              className="text-sm font-medium text-gray-800"
              title="특성값 스케일링/정규화 시 상한 기준"
            >
              maxFactor
            </label>
            <input
              id="maxFactor"
              type="number"
              step="any"
              placeholder="예: 5"
              value={maxFactor}
              onChange={(e) => setMaxFactor(e.target.value)}
              className="border p-2 rounded mt-1"
              aria-describedby="maxFactorHelp"
            />
            <p id="maxFactorHelp" className="mt-1 text-xs text-gray-500">
              특성 값의 <b>상한 기준</b>으로 사용됩니다. 예: 5
            </p>
          </div>

          {/* minFactor */}
          <div className="flex flex-col">
            <label
              htmlFor="minFactor"
              className="text-sm font-medium text-gray-800"
              title="특성값 스케일링/정규화 시 하한 기준"
            >
              minFactor
            </label>
            <input
              id="minFactor"
              type="number"
              step="any"
              placeholder="예: 2"
              value={minFactor}
              onChange={(e) => setMinFactor(e.target.value)}
              className="border p-2 rounded mt-1"
              aria-describedby="minFactorHelp"
            />
            <p id="minFactorHelp" className="mt-1 text-xs text-gray-500">
              특성 값의 <b>하한 기준</b>으로 사용됩니다. 예: 2
            </p>
          </div>
        </div>

        {/* ✅ CSV 업로드 모드 UI */}
        {mode === 'csv' && (
          <div className="mt-6 max-w-2xl mx-auto w-full">
            <div className="border rounded p-4 bg-white">
              <p className="text-sm text-gray-700 mb-2">
                CSV 파일을 선택하세요. (예:{' '}
                <code>name, column01, column02, ...</code>)
              </p>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setCsvFile(e.target.files?.[0] ?? null)}
                className="block w-full"
              />
              <div className="mt-4 flex justify-end">
                <button
                  type="button"
                  onClick={handleCsvUpload}
                  disabled={!csvFile}
                  className={`px-4 py-2 rounded ${csvFile ? 'bg-blue-600 text-white hover:bg-blue-700' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
                >
                  CSV로 서버 호출
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 유저데이터 table */}
        {mode === 'manual' && (
          <>
            <div className="mt-6 px-8 overflow-x-auto relative">
              {/* ✨ 변경: 토글 시 숨김으로 바뀌면 가중치 전부 1로 초기화 */}
              <div className="mb-2 flex justify-end">
                <button
                  onClick={() =>
                    setShowWeight((prev) => {
                      const next = !prev;
                      if (!next) {
                        // 숨김 상태로 전환될 때 가중치 전부 1로
                        setFactorWeight(Array(customColumns.length).fill(1));
                      }
                      return next;
                    })
                  }
                  className="px-3 py-1 border rounded hover:bg-gray-50"
                  type="button"
                  title="가중치 행 추가/제거"
                >
                  {showWeight ? '가중치 제거' : '가중치 추가'}
                </button>
              </div>
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
                      <th
                        key={colIdx}
                        className="border px-2 py-1 w-15 md:w-32"
                      >
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
                  {/* ✨ 추가: 가중치 행 (thead 바로 아래) */}
                  {showWeight && (
                    <tr className="bg-yellow-50">
                      {/* 이름 열에는 입력 없음(요구: name 안 받기) */}
                      <th className="border px-2 py-1 sticky left-0 z-30 bg-yellow-50 text-left">
                        가중치
                      </th>
                      {customColumns.map((_, colIdx) => (
                        <th key={colIdx} className="border px-2 py-1">
                          <input
                            type="number"
                            step="0.1"
                            value={factorWeight[colIdx] ?? 1}
                            onChange={(e) => {
                              const v = Number(e.target.value);
                              setFactorWeight((prev) => {
                                const copy = [...prev];
                                copy[colIdx] = isNaN(v) ? 0 : v;
                                return copy;
                              });
                            }}
                            className="w-full min-w-0 border rounded px-1 py-0.5 text-xs text-right"
                            placeholder="1"
                          />
                        </th>
                      ))}
                      <th className="border px-2 py-1" />
                    </tr>
                  )}
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
          </>
        )}
      </main>

      {/* 🟩 푸터 */}
      <footer className="bg-gray-200 p-4 text-center">Footer</footer>
    </div>
  );
}

export default App;
