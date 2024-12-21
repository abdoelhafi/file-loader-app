// src/test-utils.ts
import { render as rtlRender } from '@testing-library/react';
import { ToastContainer } from 'react-toastify';

function render(ui: React.ReactElement) {
  return rtlRender(
    <>
      {ui}
      <ToastContainer />
    </>
  );
}

export * from '@testing-library/react';
export { render };