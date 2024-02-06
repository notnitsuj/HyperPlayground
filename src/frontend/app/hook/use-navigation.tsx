"use client";

import { useEffect, useState } from "react";

import { usePathname } from "next/navigation";

const useNavigation = () => {
  const pathname = usePathname();
  const [IsHomeActive, setIsHomeActive] = useState(false);
  const [isAddActive, setIsAddActive] = useState(false);
  const [isJobsActive, setIsJobsActive] = useState(false);
  const [isResultsActive, setIsResultsActive] = useState(false);

  useEffect(() => {
    setIsHomeActive(false);
    setIsAddActive(false);
    setIsJobsActive(false);
    setIsResultsActive(false);

    switch (pathname) {
      case "/":
        setIsHomeActive(true);
        break;
      case "/add":
        setIsAddActive(true);
        break;
      case "/jobs":
        setIsJobsActive(true);
        break;
      case "/results":
        setIsResultsActive(true);
        break;
      default:
        break;
    }
  }, [pathname]);

  return {
    IsHomeActive,
    isAddActive,
    isJobsActive,
    isResultsActive,
  };
};

export default useNavigation;
