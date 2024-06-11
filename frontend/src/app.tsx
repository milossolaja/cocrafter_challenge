import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";
import Header from "~/components/Header";
import "./app.css";
import { QueryClient, QueryClientProvider } from "@tanstack/solid-query";

const queryClient = new QueryClient();

export default function App() {
  return (
    <Router
      root={props => (
        <>
          <Header />
          <QueryClientProvider client={queryClient}>
            <Suspense fallback={<div class={"m-12 bg-gray-200 rounded-md h-[300px]"} />}>{props.children}</Suspense>
          </QueryClientProvider>
        </>
      )}
    >
      <FileRoutes />
    </Router>
  );
}
