import React from "react";
import Stack from "@shared/components/Stack";
import Button from "@shared/components/Button";

type Props = {
  question: string;
  setQuestion: (v: string) => void;
  isPending: boolean;
  canSubmit: boolean;
  onSubmit: () => void;
  onClear: () => void;
  testId?: string;
};

export const QueryInput: React.FC<Props> = ({
  question,
  setQuestion,
  isPending,
  canSubmit,
  onSubmit,
  onClear,
  testId,
}) => {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (canSubmit) onSubmit();
      }}
    >
      <Stack spacing={1}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={4}
          style={{ width: "100%" }}
          placeholder="Ask a question, e.g., Which agreements are governed by UAE law?"
          disabled={isPending}
          data-testid={testId}
        />
        <Stack direction="row" spacing={1}>
          <Button type="submit" variant="contained" disabled={!canSubmit}>
            Send
          </Button>
          <Button variant="outlined" disabled={isPending} onClick={onClear}>
            Clear
          </Button>
        </Stack>
      </Stack>
    </form>
  );
};
