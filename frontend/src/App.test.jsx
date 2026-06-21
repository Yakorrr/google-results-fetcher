import {render, screen} from '@testing-library/react';
import {expect, test} from 'vitest';
import App from './App';

test('renders Google Search app with input field', () => {
    render(<App/>);

    // Check if the title is rendered
    const titleElement = screen.getByText(/Google Search/i);
    expect(titleElement).toBeDefined();

    // Check if input field exists
    const inputElement = screen.getByPlaceholderText(/Enter keyword/i);
    expect(inputElement).toBeDefined();
});