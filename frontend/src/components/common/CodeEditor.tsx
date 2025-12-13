import { useState } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  onLanguageChange: (lang: string) => void;
  readOnly?: boolean;
}

const languages = [
  { value: 'python', label: 'Python' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'c', label: 'C' },
];

// Simple syntax highlighting
function highlightCode(code: string, language: string) {
  const keywords: Record<string, string[]> = {
    python: ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return', 'import', 'from', 'as', 'try', 'except', 'with', 'in', 'not', 'and', 'or', 'True', 'False', 'None', 'lambda', 'yield', 'global', 'nonlocal', 'pass', 'break', 'continue', 'raise', 'assert'],
    java: ['public', 'private', 'protected', 'class', 'interface', 'extends', 'implements', 'static', 'final', 'void', 'int', 'long', 'double', 'float', 'boolean', 'char', 'String', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return', 'new', 'try', 'catch', 'finally', 'throw', 'throws', 'import', 'package', 'this', 'super', 'null', 'true', 'false'],
    cpp: ['#include', 'using', 'namespace', 'std', 'int', 'long', 'double', 'float', 'char', 'bool', 'void', 'class', 'struct', 'public', 'private', 'protected', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return', 'new', 'delete', 'try', 'catch', 'throw', 'const', 'static', 'virtual', 'override', 'nullptr', 'true', 'false', 'template', 'typename', 'auto'],
    c: ['#include', '#define', 'int', 'long', 'double', 'float', 'char', 'void', 'struct', 'typedef', 'enum', 'union', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return', 'const', 'static', 'extern', 'sizeof', 'NULL'],
  };

  const langKeywords = keywords[language] || [];
  let highlighted = code;

  // Highlight strings
  highlighted = highlighted.replace(/(["'`])(?:(?!\1)[^\\]|\\.)*\1/g, '<span class="text-neon-green">$&</span>');
  
  // Highlight comments
  highlighted = highlighted.replace(/(\/\/.*$|\/\*[\s\S]*?\*\/|#.*$)/gm, '<span class="text-muted-foreground italic">$&</span>');
  
  // Highlight numbers
  highlighted = highlighted.replace(/\b(\d+\.?\d*)\b/g, '<span class="text-neon-orange">$1</span>');

  // Highlight keywords
  langKeywords.forEach((keyword) => {
    const regex = new RegExp(`\\b(${keyword})\\b`, 'g');
    highlighted = highlighted.replace(regex, '<span class="text-primary font-bold">$1</span>');
  });

  // Highlight functions
  highlighted = highlighted.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g, '<span class="text-secondary">$1</span>(');

  return highlighted;
}

export function CodeEditor({ value, onChange, language, onLanguageChange, readOnly = false }: CodeEditorProps) {
  const lineNumbers = value.split('\n').length;

  return (
    <div className="flex flex-col h-full border border-border/50 rounded-lg overflow-hidden bg-card/50">
      <div className="flex items-center justify-between px-4 py-2 border-b border-border/50 bg-muted/30">
        <span className="text-sm text-muted-foreground font-mono">editor.{language}</span>
        <Select value={language} onValueChange={onLanguageChange} disabled={readOnly}>
          <SelectTrigger className="w-[120px] h-8 text-sm">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {languages.map((lang) => (
              <SelectItem key={lang.value} value={lang.value}>
                {lang.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="flex-1 flex overflow-auto">
        <div className="flex-shrink-0 px-3 py-4 text-right text-muted-foreground text-sm font-mono bg-muted/20 select-none border-r border-border/50">
          {Array.from({ length: lineNumbers }, (_, i) => (
            <div key={i + 1} className="leading-6">
              {i + 1}
            </div>
          ))}
        </div>

        <div className="flex-1 relative">
          {readOnly ? (
            <div
              className="absolute inset-0 px-4 py-4 font-mono text-sm leading-6 whitespace-pre overflow-auto"
              dangerouslySetInnerHTML={{ __html: highlightCode(value, language) }}
            />
          ) : (
            <>
              <div
                className="absolute inset-0 px-4 py-4 font-mono text-sm leading-6 whitespace-pre pointer-events-none overflow-auto"
                dangerouslySetInnerHTML={{ __html: highlightCode(value, language) }}
                aria-hidden="true"
              />
              <textarea
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={cn(
                  'absolute inset-0 w-full h-full px-4 py-4 font-mono text-sm leading-6',
                  'bg-transparent text-transparent caret-foreground',
                  'resize-none outline-none',
                  'whitespace-pre overflow-auto'
                )}
                spellCheck={false}
                autoCapitalize="off"
                autoCorrect="off"
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
