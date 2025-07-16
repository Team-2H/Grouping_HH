import { Button } from "./components/ui/button";
import { Card, CardContent } from "./components/ui/card";
import React from "react";

export default function App() {
  // Data for people list
  const people = [
    "사람1",
    "사람2",
    "사람3",
    "사람4",
    "사람5",
    "사람6",
    "사람7",
    "사람8",
  ];

  return (
  <div className="w-full bg-white px-8 py-6">
    {/* Header */}
    <div className="bg-[#93aafb] w-full h-16 flex items-center justify-center">
      <div className="font-normal text-black text-xl">
        영어로 제목 짓기 웹사이트 명. ex)
      </div>
    </div>

    {/* Main Title */}
    <div className="mt-10 text-5xl font-normal text-black text-center">
      공통점을 찾아 팀을 만드세요.
    </div>

    {/* Group Count & Options */}
    <div className="flex justify-center gap-6 mt-10">
      <Card className="w-[276px] h-11 bg-[#d9d9d9] border-none rounded-none">
        <CardContent className="flex items-center justify-center p-0 h-full">
          <div className="text-xl whitespace-nowrap font-normal text-black">
            그룹 개수
          </div>
        </CardContent>
      </Card>
      <Card className="w-[100px] h-[47px] bg-[#d9d9d9] border-none rounded-none">
        <CardContent className="flex items-center justify-center p-0 h-full">
          <div className="text-xl whitespace-nowrap font-normal text-black">
            추가 옵션
          </div>
        </CardContent>
      </Card>
    </div>

    {/* Advertisements */}
    <div className="flex justify-between mt-10">
      <Card className="w-[30%] h-[173px] bg-[#d9d9d9] border-none rounded-none">
        <CardContent className="flex items-center justify-center h-full">
          <div className="font-normal text-black text-[50px]">광고</div>
        </CardContent>
      </Card>
      <Card className="w-[30%] h-[173px] bg-[#d9d9d9] border-none rounded-none">
        <CardContent className="flex items-center justify-center h-full">
          <div className="font-normal text-black text-[50px]">광고</div>
        </CardContent>
      </Card>
    </div>

    {/* Main Data Section */}
    <div className="flex mt-10">
      {/* People Sidebar */}
      <div className="w-[80px] bg-[#f19f9f] flex flex-col items-center py-6 gap-2.5">
        {people.map((person, index) => (
          <div key={index} className="text-xs font-normal text-black">{person}</div>
        ))}
      </div>

      {/* Data Table */}
      <div className="flex-1 bg-[#d9d9d9]">
        <div className="bg-[#d14444] h-12 flex items-center pl-8">
          <div className="text-xl font-normal text-black">컬럼 넣는 곳</div>
        </div>
        <div className="flex items-center justify-center h-[420px]">
          <div className="text-xl font-normal text-black">
            사용자가 데이터 넣는 표
          </div>
        </div>
      </div>
    </div>

    {/* Template & Upload Section */}
    <div className="flex justify-end items-center gap-4 mt-10">
      <div className="text-xl font-normal text-black">
        양식으로 데이터를 밀어넣을 수 있습니다
      </div>
      <Button
        variant="outline"
        className="w-[184px] h-[54px] bg-[#d9d9d9] rounded-none border-none text-xl font-normal text-black"
      >
        CSV 양식 다운로드
      </Button>
      <Button
        variant="outline"
        className="w-[172px] h-[52px] bg-[#d9d9d9] rounded-none border-none text-xl font-normal text-black"
      >
        CSV 업로드
      </Button>
    </div>

    {/* Start Button */}
    <div className="flex justify-center mt-10">
      <Button
        variant="outline"
        className="w-[395px] h-[67px] bg-[#d9d9d9] rounded-none border-none text-xl font-normal text-black"
      >
        그룹핑 시작
      </Button>
    </div>
</div>

  );
}
