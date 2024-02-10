"use client";

import useSWR from "swr";

import { GET_ALL_TASKS_URL } from "../constants/backend";
import SortableTable from "@/components/sortable-table";

export default function Tasks() {
  const fetcher = (url: string) => fetch(url).then((res) => res.json());

  const { data, error, isLoading } = useSWR(GET_ALL_TASKS_URL, fetcher);

  if (error) return "An error has occurred.";
  if (isLoading) return "Loading...";

  return (
    <div className="ml-52">
      <SortableTable tasks={data} />
    </div>
  );
}
