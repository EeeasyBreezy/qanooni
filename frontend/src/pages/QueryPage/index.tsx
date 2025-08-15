import React from "react";
import PageContainer from "@shared/components/PageContainer";
import Typography from "@shared/components/Typography";
import { QueryInput } from "./components/QueryInput";
import { QueryResults } from "./components/QueryResults";
import { useQueryPage } from "./state/useQueryPage";

export const QueryPage: React.FC = () => {
  const {
    question,
    setQuestion,
    page,
    pageSize,
    isPending,
    data,
    canSubmit,
    submit,
    clear,
    onPaginationModelChange,
  } = useQueryPage();

  return (
    <PageContainer>
      <Typography variant="h4" component="h1" gutterBottom>
        Mass Interrogation
      </Typography>

      <QueryInput
        question={question}
        setQuestion={setQuestion}
        isPending={isPending}
        canSubmit={canSubmit}
        onSubmit={submit}
        onClear={clear}
        testId="query-input"
      />

      <QueryResults
        data={data}
        page={page}
        pageSize={pageSize}
        isPending={isPending}
        onPaginationModelChange={onPaginationModelChange}
      />
    </PageContainer>
  );
};

export default QueryPage;
