import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Play, Loader2, ThumbsUp, ThumbsDown, Clock, HardDrive } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { Navbar } from '@/components/layout/Navbar';
import Editor from 'react-simple-code-editor';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-cpp';
import { mockProblems } from '@/data/mockData';
import { toast } from '@/hooks/use-toast';

export default function Solve() {
  const { id } = useParams();
  const problem = mockProblems.find(p => p.id === id) || mockProblems[0];

  const allowedLanguages = ['python', 'java', 'c', 'cpp'];
  const [language, setLanguage] = useState('python');

  const [code, setCode] = useState({
    python: `def solution():\n  # Code here!\n\n\nif __name__ == "__main__":\n    solution()`,
    java: `// The class name must be Solution!\n\nimport java.util.Scanner;\n\npublic class Solution {\n  public static void main(String[] args) {\n    \n  }\n}`,
    c: `// Write your solution!\n#include <stdio.h>\n\nint main() {\n  \n  return 0;\n}`,
    cpp: `// Write your solution!\n#include <iostream>\n\nusing namespace std;\n\nint main() {\n  \n  return 0;\n}`,
  });

  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = () => {
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      const results = ['accepted', 'wrong_answer', 'time_limit'];
      const result = results[Math.floor(Math.random() * results.length)];
      toast({
        title:
          result === 'accepted'
            ? '✅ Aceito!'
            : result === 'wrong_answer'
            ? '❌ Resposta Errada'
            : '⏱️ Tempo Excedido',
        variant: result === 'accepted' ? 'default' : 'destructive',
      });
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex h-[calc(100vh-64px)]">
        {/* PROBLEM INFO */}
        <div className="w-1/2 p-4 overflow-auto border-r border-border/50">
          <Link to={`/problem/${problem.id}`}>
            <Button variant="ghost" size="sm" className="mb-4 gap-2">
              <ArrowLeft className="h-4 w-4" /> Voltar
            </Button>
          </Link>

          <Card className="border-border/50 bg-card/50">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm text-muted-foreground font-mono">#{problem.id}</span>
                  <CardTitle className="mt-1">{problem.title}</CardTitle>
                  <p className="text-sm text-muted-foreground">por {problem.creatorName}</p>
                </div>
                <DifficultyBadge difficulty={problem.difficulty} />
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="prose prose-sm prose-invert max-w-none font-mono">
                {problem.description}
              </div>

              <div className="flex gap-4 text-sm mt-4">
                <span className="flex items-center gap-1"><ThumbsUp className="h-4 w-4" />{problem.likes}</span>
                <span className="flex items-center gap-1"><ThumbsDown className="h-4 w-4" />{problem.dislikes}</span>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm mt-2">
                <div className="flex items-center gap-2 text-muted-foreground"><Clock className="h-4 w-4" /> {problem.timeLimit}ms</div>
                <div className="flex items-center gap-2 text-muted-foreground"><HardDrive className="h-4 w-4" /> {problem.memoryLimit}MB</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* SOLUTION CODE */}
        <div className="w-1/2 p-4 flex flex-col">
          {/* LANGUAGE SELECT */}
          <div className="flex gap-2 mb-2 justify-center">
            {allowedLanguages.map(lang => (
              <Button
                key={lang}
                size="sm"
                className='w-20'
                variant={language === lang ? 'default' : 'outline'}
                onClick={() => setLanguage(lang)}
              >
                {lang.toUpperCase()}
              </Button>
            ))}
          </div>

          {/* EDITOR */}
          <div className="flex-1 mb-2 overflow-auto border border-border/30 rounded-md bg-card/50">
            <Editor
              value={code[language]}
              onValueChange={(val) => setCode(prev => ({ ...prev, [language]: val }))}
              highlight={(val) => Prism.highlight(val, Prism.languages[language], language)}
              padding={16}
              style={{
                fontFamily: '"Fira Code", monospace',
                fontSize: 14,
                minHeight: '400px',
                outline: 0,
                background: 'transparent',
              }}
            />
          </div>

          <Button className="w-full gap-2 mt-2" onClick={handleSubmit} disabled={submitting}>
            {submitting
              ? <><Loader2 className="h-4 w-4 animate-spin" /> Submetendo...</>
              : <><Play className="h-4 w-4" /> Submeter</>}
          </Button>
        </div>
      </div>
    </div>
  );
}
