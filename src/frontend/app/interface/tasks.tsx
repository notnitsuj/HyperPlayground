export default interface TaskInterface {
  id: number;
  status: number;
  job_id: number;
  execute_order: number;
  checkpoint: string;
  logs: string;
  use_gpu: boolean;
  lr: number;
  train_batch_size: number;
  test_batch_size: number;
  epoch: number;
  dropout_rate: number;
  transform: string;
  optimizer: number;
  optimizer_args: string;
  scheduler: number;
  scheduler_args: string;
  cleanlab: boolean;
  accuracy: number;
  avg_precision: number;
  avg_recall: number;
  runtime: number;
  job: {
    id: number;
    queue_order: number;
    backlog_order: number;
    type: number;
    strategy: number;
  };
}
