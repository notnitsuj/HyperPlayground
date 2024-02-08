export default interface JobInterface {
  id: number;
  status: number;
  queue_order: number;
  backlog_order: number;
  type: number;
  strategy: number;
  best: number | null;
  tasks: {
    id: number;
    status: number;
    job_id: number;
    execute_order: number | null;
    checkpoint: string | null;
    logs: string | null;
    use_gpu: boolean;
    lr: number;
    train_batch_size: number;
    test_batch_size: number;
    epoch: number;
    dropout_rate: number | null;
    transform: string | null;
    optimizer: number;
    optimizer_args: string | null;
    scheduler: number | null;
    scheduler_args: string | null;
    cleanlab: boolean | null;
  }[];
}
