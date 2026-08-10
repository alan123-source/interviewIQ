import FeatureCard from "./FeatureCard";

export default function Features() {
  return (
    <section className="p-10">
      <h2 className="text-3xl font-bold">
        Features
      </h2>

      <div className="mt-6 space-y-4">
        <FeatureCard
          title="Resume Based Interviews"
          description="Generate interviews from uploaded resumes."
        />

        <FeatureCard
          title="AI Evaluation"
          description="Receive detailed AI feedback."
        />

        <FeatureCard
          title="Skill Gap Analysis"
          description="Identify missing skills."
        />
      </div>
    </section>
  );
}