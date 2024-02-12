"use client";

import { useEffect, useState } from "react";

import { usePathname } from "next/navigation";

const useNavigation = () => {
  const pathname = usePathname();
  const [IsHomeActive, setIsHomeActive] = useState(false);
  const [isAddActive, setIsAddActive] = useState(false);
  const [isTasksActive, setIsTasksActive] = useState(false);
  const [isResultsActive, setIsResultsActive] = useState(false);

  useEffect(() => {
    setIsHomeActive(false);
    setIsAddActive(false);
    setIsTasksActive(false);
    setIsResultsActive(false);

    switch (pathname) {
      case "/":
        setIsHomeActive(true);
        break;
      case "/add":
        setIsAddActive(true);
        break;
      case "/tasks":
        setIsTasksActive(true);
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
    isTasksActive,
    isResultsActive,
  };
};

export default useNavigation;
