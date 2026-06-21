import {expect, test} from 'vitest';
import {prepareJsonData} from './utils';

test('prepareJsonData returns valid formatted json string', () => {
    const mockData = {results: [{title: 'Test'}]};
    const jsonString = prepareJsonData(mockData);

    expect(typeof jsonString).toBe('string');
    expect(jsonString).toContain('"title": "Test"');
});