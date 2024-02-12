import { useMultistepForm } from "@/hook/use-multistep-form";

export default function MultiStepForm() {
  const {
    currentStepIndex,
    step,
    steps,
    isFirstStep,
    isLastStep,
    goTo,
    next,
    back,
  } = useMultistepForm([]);

  return <div></div>;
}
