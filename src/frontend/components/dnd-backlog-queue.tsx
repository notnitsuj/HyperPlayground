"use client";

import {
  DragDropContext,
  DropResult,
  Droppable,
  Draggable,
} from "@hello-pangea/dnd";
import useSWR from "swr";

import { GET_ALL_JOBS_URL, REORDER_JOB_URL } from "@/app/constants/backend";
import JobInterface from "@/app/interface/jobs";

export default function BacklogQueue() {
  const fetcher = (url: string) => fetch(url).then((res) => res.json());

  const { data, error, isLoading, mutate } = useSWR(GET_ALL_JOBS_URL, fetcher);

  if (error) return "An error has occurred.";
  if (isLoading) return "Loading...";

  var backlogJobs: JobInterface[] = [];
  var queueJobs: JobInterface[] = [];

  for (var job of data) {
    if (job.status === 0) backlogJobs.push(job);
    if (job.status === 1) queueJobs.push(job);
  }

  backlogJobs.sort((a, b) => a.backlog_order - b.backlog_order);
  queueJobs.sort((a, b) => a.queue_order - b.queue_order);

  const onDragEnd = async (result: DropResult) => {
    const { source, destination, draggableId } = result;

    if (!destination) return;

    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    )
      return;

    const reorderData = {
      job_id: draggableId,
      new_status: destination.droppableId,
      new_order: destination.index,
    };

    const response = await fetch(REORDER_JOB_URL, {
      method: "PATCH",
      body: JSON.stringify(reorderData),
    });

    mutate();
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex gap-4">
        <Droppable droppableId="BACKLOG">
          {(provided) => (
            <div
              className="p-2 mt-5 w-80 bg-white border-gray-400 border border-dashed"
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <h2 className="text-center font-bold text-black">BACKLOG</h2>
              <div>
                {backlogJobs.map((job: JobInterface) => (
                  <Draggable
                    key={`draggableId-${job.id}`}
                    draggableId={`draggableId-${job.id}`}
                    index={job.backlog_order}
                  >
                    {(provided) => (
                      <div
                        className="bg-gray-200 mx-1 px-4 py-3 my-3"
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                      >
                        <div>{job.id}</div>
                      </div>
                    )}
                  </Draggable>
                ))}
              </div>

              {provided.placeholder}
            </div>
          )}
        </Droppable>

        <Droppable droppableId="QUEUE">
          {(provided) => (
            <div
              className="p-2 mt-5 w-80 bg-white  border-gray-400 border border-dashed"
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <h2 className="text-center font-bold text-black">QUEUE</h2>
              <div>
                {queueJobs.map((job: JobInterface) => (
                  <Draggable
                    key={`draggableId-${job.id}`}
                    draggableId={`draggableId-${job.id}`}
                    index={job.queue_order}
                  >
                    {(provided) => (
                      <div
                        className="bg-gray-200 mx-1 px-4 py-3 my-3"
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                      >
                        <div>{job.id}</div>
                      </div>
                    )}
                  </Draggable>
                ))}
              </div>

              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </div>
    </DragDropContext>
  );
}
