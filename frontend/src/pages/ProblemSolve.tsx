import { Link, useParams } from 'react-router-dom'
import {
  ArrowLeft,
  Clock,
  HardDrive,
  Cpu,
  Code2,
  CheckCircle,
  MessageSquare,
  Send,
} from 'lucide-react'

import { PageContainer } from '@/components/layout/PageContainer'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Textarea } from '@/components/ui/textarea'
import { DifficultyBadge } from '@/components/ui/DifficultyBadge'
import { TagBadge } from '@/components/ui/TagBadge'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { useState } from 'react'


import {
  mockProblems,
  mockSubmissions,
  problemTags,
  mockSolveComments,
} from '@/data/mockData'

export default function ProblemSolve() {
  const { problemId, solveId } = useParams()
  const [replyingTo, setReplyingTo] = useState<string | null>(null)

  const problem =
    mockProblems.find(p => p.id === problemId) || mockProblems[0]

  const solve =
    mockSubmissions.find(s => s.id === solveId) || mockSubmissions[0]

  const comments = mockSolveComments.filter(
    c => c.solveId === solve.id
  )

  const parentComments = comments.filter(c => !c.parentId)
  const getReplies = (id: string) =>
    comments.filter(c => c.parentId === id)

  const getTagColor = (t: string) =>
    (problemTags.find(pt => pt.name === t)?.color as any) || 'purple'

  return (
    <PageContainer>
      <Link to={`/problem/${problem.id}`}>
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />
          Voltar para o problema
        </Button>
      </Link>

      <div className="grid lg:grid-cols-3 gap-6 items-start">

        {/* ================= MAIN ================= */}
        <div className="lg:col-span-2 space-y-6">

          {/* PROBLEM SUMMARY */}
          <Card className="border-border/50 bg-card/50 pixel-card">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-sm text-muted-foreground font-mono">
                    #{problem.id}
                  </span>
                  <h1 className="text-xl font-bold mt-1">
                    {problem.title}
                  </h1>
                  <p className="text-muted-foreground text-sm">
                    por {problem.creatorName}
                  </p>
                </div>
                <DifficultyBadge difficulty={problem.difficulty} />
              </div>
            </CardHeader>

            <CardContent>
              <p className="text-foreground/90 mb-4">
                {problem.description}
              </p>

              <div className="flex flex-wrap gap-2">
                {problem.tags.map(t => (
                  <TagBadge
                    key={t}
                    tag={t}
                    color={getTagColor(t)}
                  />
                ))}
              </div>
            </CardContent>
          </Card>

          {/* SOLUTION CODE */}
          <Card className="border-border/50 bg-card/50 pixel-card pixel-scanlines">
            <CardHeader className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2 font-arcade text-sm">
                <Code2 className="h-5 w-5 text-primary" />
                Solução
              </CardTitle>
              <span className="text-xs font-mono text-muted-foreground">
                {solve.language}
              </span>
            </CardHeader>

            <CardContent>
              <SyntaxHighlighter
                language={solve.language.toLowerCase()}
                style={oneDark}
                showLineNumbers
                customStyle={{
                    background: 'transparent',
                    padding: '1rem',
                    margin: 0,
                    fontSize: '0.75rem',
                }}
                codeTagProps={{
                    style: {
                    background: 'transparent',
                    },
                }}
                lineNumberStyle={{
                    color: '#6b7280',
                    marginRight: '12px',
                }}
                className="rounded-lg border border-border/40 bg-background/60"
                >
                {solve.code}
                </SyntaxHighlighter>
            </CardContent>
          </Card>

          {/* COMMENTS */}
          <Card className="border-border/50 bg-card/50 pixel-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 font-arcade text-sm">
                <MessageSquare className="h-5 w-5 text-primary" />
                Comentários ({comments.length})
              </CardTitle>
            </CardHeader>

            <CardContent className="space-y-5">

              {/* INPUT */}
              <div className="flex gap-3">
                <Avatar className="h-9 w-9">
                  <AvatarFallback>U</AvatarFallback>
                </Avatar>

                <div className="flex-1 space-y-2">
                  <Textarea
                    placeholder="Adicione um comentário..."
                    className="resize-none min-h-[70px]"
                  />
                  <div className="flex justify-end">
                    <Button size="sm" className="pixel-btn gap-2">
                      <Send className="h-4 w-4" />
                      Publicar
                    </Button>
                  </div>
                </div>
              </div>

              {/* LIST */}
              <div className="space-y-6 pt-4 border-t border-border/30">
                {parentComments.map(comment => (
                  <div key={comment.id} className="space-y-3">

                    {/* PARENT */}
                    <div className="flex gap-3">
                      <Avatar className="h-9 w-9">
                        <AvatarImage src={comment.userAvatar} />
                        <AvatarFallback>
                          {comment.userName.charAt(0)}
                        </AvatarFallback>
                      </Avatar>

                      <div className="flex-1">
                        <div className="bg-background/60 rounded-lg px-3 py-2">
                          <Link
                            to={`/user/${comment.userId}`}
                            className="text-sm font-semibold hover:text-primary"
                          >
                            {comment.userName}
                          </Link>
                          <p className="text-sm">
                            {comment.content}
                          </p>
                        </div>

                        <button
                        className="text-xs text-muted-foreground mt-1 hover:text-primary"
                        onClick={() =>
                            setReplyingTo(replyingTo === comment.id ? null : comment.id)
                        }
                        >
                        Responder
                        </button>

                        {replyingTo === comment.id && (
                            <div className="flex gap-3 mt-2 ml-12">
                                <Avatar className="h-8 w-8">
                                <AvatarFallback>U</AvatarFallback>
                                </Avatar>
                                <div className="flex-1 space-y-1">
                                <Textarea
                                    placeholder="Escreva sua resposta..."
                                    className="resize-none min-h-[60px]"
                                />
                                <div className="flex justify-end">
                                    <Button size="sm" className="pixel-btn gap-2">
                                    <Send className="h-2 w-2" /> Publicar
                                    </Button>
                                </div>
                                </div>
                            </div>
                            )}
                      </div>
                    </div>

                    {/* REPLIES */}
                    {getReplies(comment.id).map(reply => (
                      <div key={reply.id} className="flex gap-3 ml-12">
                        <Avatar className="h-8 w-8">
                          <AvatarImage src={reply.userAvatar} />
                          <AvatarFallback>
                            {reply.userName.charAt(0)}
                          </AvatarFallback>
                        </Avatar>

                        <div className="flex-1 bg-background/50 rounded-lg px-3 py-2">
                          <Link
                            to={`/user/${reply.userId}`}
                            className="text-sm font-semibold hover:text-primary"
                          >
                            {reply.userName}
                          </Link>
                          <p className="text-sm">
                            {reply.content}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* ================= SIDEBAR ================= */}
        <div className="space-y-4">

          {/* AUTHOR */}
          <Card className="border-border/50 bg-card/50 pixel-card">
            <CardContent className="pt-6 flex items-center gap-3">
              <Avatar className="h-12 w-12 ring-2 ring-primary/30">
                <AvatarImage src={solve.odAvatar} />
                <AvatarFallback>
                  {solve.odName.charAt(0)}
                </AvatarFallback>
              </Avatar>

              <div>
                <Link
                  to={`/user/${solve.odId}`}
                  className="font-semibold hover:text-primary"
                >
                  {solve.odName}
                </Link>
                <p className="text-xs text-muted-foreground">
                  Autor da solução
                </p>
              </div>
            </CardContent>
          </Card>

          {/* STATS */}
          <Card className="border-border/50 bg-card/50 pixel-card">
            <CardContent className="pt-6 space-y-3">
              <div className="flex justify-between">
                <span className="flex gap-2 text-muted-foreground">
                  <Clock className="h-4 w-4" /> Tempo
                </span>
                <span>{solve.time} ms</span>
              </div>

              <div className="flex justify-between">
                <span className="flex gap-2 text-muted-foreground">
                  <HardDrive className="h-4 w-4" /> Memória
                </span>
                <span>{solve.memory} MB</span>
              </div>

              <div className="flex justify-between">
                <span className="flex gap-2 text-muted-foreground">
                  <Cpu className="h-4 w-4" /> Linguagem
                </span>
                <span>{solve.language}</span>
              </div>

              <div className="flex justify-between">
                <span className="flex gap-2 text-muted-foreground">
                  <CheckCircle className="h-4 w-4" /> Status
                </span>
                <span className="text-neon-green font-semibold">
                  ACEITO
                </span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageContainer>
  )
}
