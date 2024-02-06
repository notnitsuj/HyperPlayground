"use client";

import React from "react";

import Link from "next/link";

import useNavigation from "@/app/hook/use-navigation";
import { Icon } from "@iconify/react";

const SideNav = () => {
  const { IsHomeActive, isAddActive, isJobsActive, isResultsActive } =
    useNavigation();

  return (
    <div className="flex-col space-y-4 items-center px-4 py-8 hidden sm:flex border-r border-zinc-700 h-full  w-[120px] md:w-[200px] md:items-start fixed">
      <Link
        href="/"
        className="flex flex-row space-x-4 items-center px-4 py-3 rounded-full duration-200 hover:bg-black/10 relative"
      >
        {IsHomeActive ? (
          <Icon icon="ic:round-dashboard" width="38" height="38" />
        ) : (
          <Icon icon="humbleicons:dashboard" width="38" height="38" />
        )}
        <span
          className={`text-2xl hidden md:flex ${
            IsHomeActive ? "font-bold" : ""
          }`}
        >
          Home
        </span>
      </Link>

      <Link
        href="/add"
        className="flex flex-row space-x-4 items-center px-4 py-3 rounded-full duration-200 hover:bg-black/10"
      >
        <Icon icon="oui:ml-create-advanced-job" width="38" height="38" />
        <span
          className={`text-2xl align-middle hidden md:flex ${
            isAddActive ? "font-bold" : ""
          }`}
        >
          Add
        </span>
      </Link>

      <Link
        href="/jobs"
        className="flex flex-row space-x-4 items-center px-4 py-3 rounded-full duration-200 hover:bg-black/10"
      >
        <Icon icon="carbon:batch-job" width="38" height="38" />
        <span
          className={`text-2xl hidden md:flex ${
            isJobsActive ? "font-bold" : ""
          }`}
        >
          Jobs
        </span>
      </Link>

      <Link
        href="/results"
        className="flex flex-row space-x-4 items-center px-4 py-3 rounded-full duration-200 hover:bg-black/10"
      >
        {isResultsActive ? (
          <Icon icon="uil:chart-line" width="38" height="38" />
        ) : (
          <Icon icon="carbon:chart-line" width="38" height="38" />
        )}
        <span
          className={`text-2xl hidden md:flex ${
            isResultsActive ? "font-bold" : ""
          }`}
        >
          Results
        </span>
      </Link>
    </div>
  );
};

export default SideNav;
