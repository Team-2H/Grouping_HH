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

  // ⬇⬇⬇ 업로드 모드 / 파일 상태 / CSV 엔드포인트
  const [mode, setMode] = useState<'manual' | 'csv'>('manual');
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const CSV_ENDPOINT = 'http://127.0.0.1:5000/groupingByCSV';

  // ✨ 가중치
  const [showWeight, setShowWeight] = useState(false); // 가중치 행 표시/숨김
  const [factorWeight, setFactorWeight] = useState<number[]>(
    Array(customColumns.length).fill(1) // 기본 가중치 1
  );

  // ✨ 컬럼명을 서버로 보낼 키로 변환
  const toKey = (label: string) =>
    label
      .trim()
      .toLowerCase()
      .replace(/[\s\-]+/g, '_') // 공백/하이픈 → _
      .replace(/[^\w]/g, '') // 영문/숫자/언더스코어만
      .replace(/^(\d)/, '_$1'); // 숫자로 시작하면 앞에 _

  // 고정 폭(px)
  const NAME_COL_PX = 140; // "이름" 열 (조금 여유)
  const ADD_COL_PX = 120; // "+ 열 추가" 열

  // 남은 폭을 중간 컬럼 개수로 균등 분배
  const middleColWidth = `calc((100% - ${NAME_COL_PX + ADD_COL_PX}px) / ${
    customColumns.length || 1
  })`;

  // ⏳ 로딩 오버레이
  const [isLoading, setIsLoading] = useState(false);
  const MIN_SPINNER_MS = 1000; // 최소 1초

  const withLoading = async (task: () => Promise<void>) => {
    setIsLoading(true);
    const start = Date.now();
    try {
      await task();
    } finally {
      const elapsed = Date.now() - start;
      const remain = MIN_SPINNER_MS - elapsed;
      if (remain > 0) setTimeout(() => setIsLoading(false), remain);
      else setIsLoading(false);
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
    setFactorWeight((prev) => [...prev, 1]);
  };

  const removeColumn = (colIdx: number) => {
    const newCols = customColumns.filter((_, idx) => idx !== colIdx);
    setCustomColumns(newCols);

    const newUserData = userData.map((user) => ({
      ...user,
      values: user.values.filter((_, idx) => idx !== colIdx),
    }));
    setUserData(newUserData);
    setFactorWeight((prev) => prev.filter((_, idx) => idx !== colIdx));
  };

  const removeUserRow = (rowIdx: number) => {
    const newUserData = userData.filter((_, idx) => idx !== rowIdx);
    setUserData(newUserData);
  };

  const handleCsvUpload = async () => {
    if (!csvFile) {
      alert('CSV 파일을 선택해 주세요.');
      return;
    }

    const formData = new FormData();
    formData.append('csvData', csvFile, csvFile.name);
    if (groupCount) formData.append('groupCount', String(groupCount));
    if (maxFactor) formData.append('maxFactor', String(maxFactor));
    if (minFactor) formData.append('minFactor', String(minFactor));

    try {
      await withLoading(async () => {
        const res = await fetch(CSV_ENDPOINT, {
          method: 'POST',
          body: formData,
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
    const keys = customColumns.map(toKey);

    const factorWeightObj: Record<string, number> = {};
    keys.forEach((k, i) => {
      factorWeightObj[k] = Number(factorWeight[i] ?? 1);
    });

    const processedUserData = userData.map((user) => {
      const obj: Record<string, any> = { name: user.name };
      keys.forEach((k, i) => {
        obj[k] = Number(user.values[i]);
      });
      return obj;
    });

    const payload: Record<string, any> = {
      groupCount: Number(groupCount),
      maxFactor: Number(maxFactor),
      minFactor: Number(minFactor),
      userData: processedUserData,
    };

    if (showWeight) {
      const factorWeightObj: Record<string, number> = {};
      keys.forEach(
        (k, i) => (factorWeightObj[k] = Number(factorWeight[i] ?? 1))
      );
      const anyNotOne = Object.values(factorWeightObj).some((v) => v !== 1);
      if (anyNotOne) payload.factorWeight = [factorWeightObj];
    }

    try {
      await withLoading(async () => {
        const res = await fetch('http://127.0.0.1:5000/grouping', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        setMessage(normalizeLabels(data.labels));
      });
    } catch (e) {
      console.error('서버 호출 실패:', e);
    }
  };

  // 파일명 표시용 헬퍼
  const fileLabel = csvFile ? csvFile.name : '선택된 파일이 없습니다';

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Top Bar */}
      <header className="sticky top-0 z-40 border-b border-slate-200 bg-gradient-to-r from-indigo-600 via-indigo-500 to-sky-500 text-white">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center font-bold">
              T
            </div>
            <span className="text-lg font-semibold tracking-tight">
              Make Common Team
            </span>
          </div>
          <nav className="hidden sm:flex items-center gap-4 text-sm">
            <span className="opacity-90">Make Common Team</span>
          </nav>
        </div>
      </header>

      {/* LOADING OVERLAY */}
      {isLoading && (
        <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm">
          <div
            className="w-16 h-16 rounded-full border-4 border-slate-300 border-t-indigo-600 animate-spin"
            aria-hidden="true"
          />
          <p className="mt-4 text-slate-800 font-medium">분석 중…</p>
          <p className="text-xs text-slate-500 mt-1">
            잠시만 기다려주세요 (≈1초)
          </p>
        </div>
      )}

      {/* Main */}
      <main className="mx-auto max-w-6xl px-4 py-8">
        {/* Title */}
        <div className="mb-6">
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
            팀 메이킹 & 클러스터링
          </h1>
          <p className="text-sm text-slate-600 mt-1">
            CSV 업로드 또는 수동 입력으로 데이터를 보내 클러스터 결과를
            확인하세요.
          </p>
        </div>

        {/* MODE TABS */}
        <div className="mb-6 inline-flex rounded-2xl bg-white p-1 shadow-sm ring-1 ring-slate-200">
          <button
            type="button"
            onClick={() => setMode('manual')}
            aria-pressed={mode === 'manual'}
            className={`px-4 py-2 rounded-xl text-sm transition ${
              mode === 'manual'
                ? 'bg-indigo-600 text-white shadow'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            수동 입력
          </button>
          <button
            type="button"
            onClick={() => setMode('csv')}
            aria-pressed={mode === 'csv'}
            className={`px-4 py-2 rounded-xl text-sm transition ${
              mode === 'csv'
                ? 'bg-indigo-600 text-white shadow'
                : 'text-slate-700 hover:bg-slate-50'
            }`}
          >
            CSV 업로드
          </button>
        </div>

        {/* PARAMS CARD */}
        <section className="mb-6 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
          <h2 className="text-base font-semibold text-slate-900">
            공통 파라미터
          </h2>
          <p className="text-xs text-slate-500 mb-4">
            클러스터 개수와 스케일링 기준을 설정합니다.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* groupCount */}
            <div className="flex flex-col">
              <label
                htmlFor="groupCount"
                className="text-sm font-medium text-slate-800"
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
                className="mt-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm outline-none focus:ring-2 focus:ring-indigo-500"
                aria-describedby="groupCountHelp"
              />
              <p id="groupCountHelp" className="mt-1 text-xs text-slate-500">
                만들 팀의 <b>최대 개수</b>를 제한합니다. 비워두면 기본값을
                사용합니다.
              </p>
            </div>
            {/* maxFactor */}
            <div className="flex flex-col">
              <label
                htmlFor="maxFactor"
                className="text-sm font-medium text-slate-800"
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
                className="mt-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm outline-none focus:ring-2 focus:ring-indigo-500"
                aria-describedby="maxFactorHelp"
              />
              <p id="maxFactorHelp" className="mt-1 text-xs text-slate-500">
                특성 값의 <b>상한 기준</b>으로 사용됩니다. 예: 5
              </p>
            </div>
            {/* minFactor */}
            <div className="flex flex-col">
              <label
                htmlFor="minFactor"
                className="text-sm font-medium text-slate-800"
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
                className="mt-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm outline-none focus:ring-2 focus:ring-indigo-500"
                aria-describedby="minFactorHelp"
              />
              <p id="minFactorHelp" className="mt-1 text-xs text-slate-500">
                특성 값의 <b>하한 기준</b>으로 사용됩니다. 예: 2
              </p>
            </div>
          </div>
        </section>

        {/* CSV UPLOAD CARD */}
        {mode === 'csv' && (
          <section className="mb-8 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
            <h2 className="text-base font-semibold text-slate-900">
              CSV 업로드
            </h2>
            <p className="text-xs text-slate-500 mb-4">
              첫 행에 컬럼 이름을 포함하세요. 예:{' '}
              <code>name, column01, column02, ...</code>
            </p>

            <div className="grid gap-4 md:grid-cols-[1fr_auto] items-end">
              <div>
                <label className="block text-sm font-medium text-slate-800 mb-1">
                  CSV 파일
                </label>
                <div className="flex items-center gap-3">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setCsvFile(e.target.files?.[0] ?? null)}
                    className="block w-full text-sm file:mr-3 file:rounded-lg file:border-0 file:bg-indigo-50 file:px-3 file:py-2 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer"
                  />
                </div>
                <p className="mt-1 text-xs text-slate-500">{fileLabel}</p>
              </div>

              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={handleCsvUpload}
                  disabled={!csvFile || isLoading}
                  className={`inline-flex items-center justify-center rounded-xl px-5 py-2.5 text-sm font-medium transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 ${
                    !csvFile || isLoading
                      ? 'bg-slate-200 text-slate-500 cursor-not-allowed'
                      : 'bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:ring-indigo-600'
                  }`}
                >
                  업로드 & 분석
                </button>
              </div>
            </div>
          </section>
        )}

        {/* MANUAL INPUT TABLE */}
        {mode === 'manual' && (
          <section className="mb-8 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-base font-semibold text-slate-900">
                데이터 입력
              </h2>
              <button
                onClick={() =>
                  setShowWeight((prev) => {
                    const next = !prev;
                    if (!next)
                      setFactorWeight(Array(customColumns.length).fill(1));
                    return next;
                  })
                }
                className="rounded-xl border border-slate-300 bg-white px-3 py-1.5 text-sm hover:bg-slate-50"
                type="button"
                title="가중치 행 추가/제거"
              >
                {showWeight ? '가중치 제거' : '가중치 추가'}
              </button>
            </div>

            <div className="overflow-x-auto rounded-xl border border-slate-200">
              <table className="w-full table-auto text-sm border-separate border-spacing-0">
                <colgroup>
                  <col style={{ width: NAME_COL_PX }} />
                  {customColumns.map((_, i) => (
                    <col key={i} style={{ width: middleColWidth }} />
                  ))}
                  <col style={{ width: ADD_COL_PX }} />
                </colgroup>
                <thead className="bg-slate-50 sticky top-0 z-20">
                  <tr className="text-slate-700">
                    <th
                      className="border-b border-slate-200 px-3 py-2 sticky left-0 top-0 z-40 bg-slate-50 text-left"
                      style={{ minWidth: '10rem' }}
                    >
                      이름
                    </th>
                    {customColumns.map((col, colIdx) => (
                      <th
                        key={colIdx}
                        className="border-b border-slate-200 px-3 py-2"
                      >
                        <div className="flex items-center gap-2">
                          <input
                            value={col}
                            onChange={(e) =>
                              handleColumnNameChange(colIdx, e.target.value)
                            }
                            className="flex-1 min-w-0 rounded-md border border-slate-300 px-2 py-1 text-xs shadow-sm focus:ring-2 focus:ring-indigo-500"
                          />
                          <button
                            onClick={() => removeColumn(colIdx)}
                            className="shrink-0 rounded-md px-2 py-1 text-red-600 hover:bg-red-50"
                            aria-label={`컬럼 ${colIdx + 1} 삭제`}
                            title="열 삭제"
                          >
                            ✕
                          </button>
                        </div>
                      </th>
                    ))}
                    <th className="border-b border-slate-200 px-3 py-2 whitespace-nowrap text-left">
                      <button
                        onClick={addColumn}
                        className="text-indigo-600 hover:underline"
                      >
                        + 열 추가
                      </button>
                    </th>
                  </tr>
                  {showWeight && (
                    <tr className="bg-amber-50 text-slate-700">
                      <th className="border-b border-slate-200 px-3 py-2 sticky left-0 z-30 bg-amber-50 text-left">
                        가중치
                      </th>
                      {customColumns.map((_, colIdx) => (
                        <th
                          key={colIdx}
                          className="border-b border-slate-200 px-3 py-2"
                        >
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
                            className="w-full min-w-0 rounded-md border border-amber-200 px-2 py-1 text-xs text-right shadow-sm focus:ring-2 focus:ring-amber-500"
                            placeholder="1"
                          />
                        </th>
                      ))}
                      <th className="border-b border-slate-200 px-3 py-2" />
                    </tr>
                  )}
                </thead>

                <tbody>
                  {userData.map((user, rowIdx) => (
                    <tr
                      key={rowIdx}
                      className={rowIdx % 2 ? 'bg-white' : 'bg-slate-50/40'}
                    >
                      <td className="px-3 py-2 sticky left-0 z-10 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/60 border-b border-slate-100">
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => removeUserRow(rowIdx)}
                            className="shrink-0 rounded-md px-2 py-1 text-red-600 hover:bg-red-50"
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
                            className="w-full rounded-md border border-slate-300 px-2 py-1 text-sm shadow-sm focus:ring-2 focus:ring-indigo-500"
                          />
                        </div>
                      </td>
                      {user.values.map((val, colIdx) => (
                        <td
                          key={colIdx}
                          className="px-3 py-2 border-b border-slate-100"
                        >
                          <input
                            value={val}
                            onChange={(e) =>
                              handleValueChange(rowIdx, colIdx, e.target.value)
                            }
                            className="w-full min-w-0 rounded-md border border-slate-300 px-2 py-1 text-xs shadow-sm focus:ring-2 focus:ring-indigo-500"
                          />
                        </td>
                      ))}
                      <td className="px-3 py-2 border-b border-slate-100" />
                    </tr>
                  ))}
                  <tr>
                    <td
                      colSpan={customColumns.length + 2}
                      className="text-center py-3"
                    >
                      <button
                        onClick={addUserRow}
                        className="rounded-xl bg-emerald-600 px-4 py-2 text-white shadow hover:bg-emerald-700"
                      >
                        + 행 추가
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* submit 버튼 */}
            <div className="mt-6 flex justify-center">
              <button
                onClick={handleButtonClick}
                disabled={isLoading}
                className={`inline-flex items-center justify-center rounded-xl px-6 py-2.5 text-sm font-medium transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 ${
                  isLoading
                    ? 'bg-slate-200 text-slate-500 cursor-not-allowed'
                    : 'bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:ring-indigo-600'
                }`}
              >
                서버 호출
              </button>
            </div>
          </section>
        )}

        {/* SERVER RESPONSE */}
        {message.length > 0 && (
          <section className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
            <h3 className="font-semibold mb-4 text-lg text-slate-900">
              서버 응답 (클러스터 결과)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {message.map((team) => (
                <div
                  key={team.cluster}
                  className="p-4 rounded-xl ring-1 ring-slate-200 bg-gradient-to-br from-slate-50 to-white shadow-sm"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="inline-flex items-center gap-2">
                      <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-white text-xs font-semibold">
                        {team.cluster + 1}
                      </span>
                      <p className="font-semibold text-slate-900">팀</p>
                    </div>
                    <span className="text-xs text-slate-600 inline-flex items-center gap-1 bg-slate-100 px-2 py-1 rounded-full">
                      인원 {team.members.length}명
                    </span>
                  </div>
                  <ul className="space-y-1">
                    {team.members.map((name, i) => (
                      <li
                        key={`${team.cluster}-${i}`}
                        className="flex items-center gap-2"
                      >
                        <span className="inline-block w-1.5 h-1.5 rounded-full bg-indigo-500" />
                        <span className="text-sm text-slate-800">{name}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-10 border-t border-slate-200 bg-white/60">
        <div className="mx-auto max-w-6xl px-4 py-4 text-center text-xs text-slate-500">
          © {new Date().getFullYear()} Grouping HH · Built with React +
          Tailwind
        </div>
      </footer>
    </div>
  );
}

export default App;
