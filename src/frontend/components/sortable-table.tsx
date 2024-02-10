"use client";

import { useState, useCallback, MouseEventHandler } from "react";
import TaskInterface from "@/app/interface/tasks";

type SortOrder = "ascn" | "desc";

type SortKeys = keyof TaskInterface;

function sortData({
  tableData,
  sortKey,
  reverse,
}: {
  tableData: TaskInterface[];
  sortKey: SortKeys;
  reverse: boolean;
}) {
  if (!sortKey) return tableData;

  const sortedData = tableData.sort((a: TaskInterface, b: TaskInterface) => {
    return a[sortKey] > b[sortKey] ? 1 : -1;
  });

  if (reverse) {
    return sortedData.reverse();
  }

  return sortedData;
}

function SortButton({
  sortOrder,
  columnKey,
  sortKey,
  onClick,
}: {
  sortOrder: SortOrder;
  columnKey: SortKeys;
  sortKey: SortKeys;
  onClick: MouseEventHandler<HTMLButtonElement>;
}) {
  return (
    <button
      onClick={onClick}
      className={`${
        sortKey === columnKey && sortOrder === "desc" ? " rotate-180" : ""
      }`}
    >
      ▲
    </button>
  );
}

export default function SortableTable({ tasks }: { tasks: TaskInterface[] }) {
  const [sortKey, setSortKey] = useState<SortKeys>("id");
  const [sortOrder, setSortOrder] = useState<SortOrder>("ascn");

  const sortedData = useCallback(
    () =>
      sortData({ tableData: tasks, sortKey, reverse: sortOrder === "desc" }),
    [tasks, sortKey, sortOrder]
  );

  const headers: { key: SortKeys; label: string }[] = [
    { key: "id", label: "ID" },
    { key: "status", label: "Task Status" },
    { key: "job_id", label: "Job" },
    { key: "lr", label: "Learning rate" },
    { key: "train_batch_size", label: "Batch size (train)" },
    { key: "test_batch_size", label: "Batch size (test)" },
    { key: "epoch", label: "epoch" },
    { key: "dropout_rate", label: "Dropout rate" },
    { key: "optimizer", label: "Optimizer" },
    { key: "scheduler", label: "Scheduler" },
    { key: "accuracy", label: "Accuracy" },
    { key: "avg_precision", label: "Average Precision" },
    { key: "avg_recall", label: "Average Recall" },
    { key: "runtime", label: "Runtime" },
  ];

  const sortableHeaders = [
    "id",
    "accuracy",
    "avg_precision",
    "avg_recall",
    "runtime",
  ];

  function changeSort(key: SortKeys) {
    setSortOrder(sortOrder === "ascn" ? "desc" : "ascn");

    setSortKey(key);
  }

  return (
    <table className="w-full text-sm text-left rtl:text-right text-black">
      <caption className="p-5 text-xl font-semibold text-left rtl:text-right text-gray-900 bg-white">
        ALL TASKS
        <p className="mt-1 text-sm font-normal text-black">
          Browse the list of tasks that have been created. Tasks can be sorted
          by ID, accuracy, average precision, average recall and runtime.
        </p>
      </caption>
      <thead className="text-sm text-black uppercase bg-white">
        <tr>
          {headers.map((row) => {
            return (
              <td key={row.key}>
                {row.label}{" "}
                {sortableHeaders.includes(row.key) && (
                  <SortButton
                    columnKey={row.key}
                    onClick={() => changeSort(row.key)}
                    {...{
                      sortOrder,
                      sortKey,
                    }}
                  />
                )}
              </td>
            );
          })}
        </tr>
      </thead>

      <tbody>
        {sortedData().map((task) => {
          return (
            <tr key={task.id} className="bg-white border-b hover:bg-gray-50 ">
              <td>{task.id}</td>
              <td>{task.status}</td>
              <td>{task.job_id}</td>
              <td>{task.lr}</td>
              <td>{task.train_batch_size}</td>
              <td>{task.test_batch_size}</td>
              <td>{task.epoch}</td>
              <td>{task.dropout_rate}</td>
              <td>{task.optimizer}</td>
              <td>{task.scheduler}</td>
              <td>{task.accuracy}</td>
              <td>{task.avg_precision}</td>
              <td>{task.avg_recall}</td>
              <td>{task.runtime}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
