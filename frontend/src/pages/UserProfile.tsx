import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import {
  ArrowLeft,
  UserPlus,
  MapPin,
  Users,
  Trophy,
  CheckCircle,
  Lightbulb,
  Gamepad2,
} from 'lucide-react'

import { PageContainer } from '@/components/layout/PageContainer'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { DifficultyBadge } from '@/components/ui/DifficultyBadge'

import { mockUsers, mockProblems } from '@/data/mockData'

import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default function UserProfile() {
  const { id } = useParams()
  const user = mockUsers.find(u => u.id === id) || mockUsers[0]
  const [activeTab, setActiveTab] = useState<'solved' | 'created'>('solved')

  const solvedProblems = mockProblems.slice(
    0,
    Math.min(user.problemsSolved, mockProblems.length),
  )

  const createdProblems = mockProblems.filter(
    p => p.creatorId === user.id,
  )

  const html = DOMPurify.sanitize(marked.parse(user.description ?? ''))

  return (
    <PageContainer>
      <Link to="/users">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
      </Link>

      <div className="grid lg:grid-cols-3 gap-6 items-start">

        {/* ================= PROFILE CARD ================= */}
        <Card className="lg:col-span-1 border-border/50 bg-card/50 pixel-card">
          <CardContent className="pt-6 flex flex-col items-center gap-4">

            <Avatar className="h-24 w-24 ring-4 ring-secondary/30">
              <AvatarImage src={user.avatar} />
              <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
            </Avatar>

            <div className="text-center">
              <h2 className="text-xl font-arcade font-bold text-glow-purple text-flicker">
                {user.name}
              </h2>
              <p className="text-sm font-mono text-muted-foreground">
                @{user.login}
              </p>
            </div>

            <div className="w-full space-y-2 text-sm text-muted-foreground">
              <div className="flex justify-center items-center gap-2">
                <MapPin className="h-4 w-4" />
                <span>{user.country}</span>
              </div>

              <div className="flex justify-center items-center gap-2">
                <Trophy className="h-4 w-4" />
                <span>{user.problemsSolved} resolvidos</span>
              </div>

              <div className="flex justify-center items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                <span className="font-semibold text-foreground">
                  {user.followers}
                </span>
                <span>seguidores</span>
              </div>
            </div>

            <Button className="w-full gap-2 pixel-btn">
              <UserPlus className="h-4 w-4" />
              Seguir
            </Button>

            {/* ================= BIO ================= */}
            {user.description && (
              <div className="w-full mt-2 border-t border-border/40 pt-3">
                <p className="mb-1 text-[10px] tracking-widest text-muted-foreground/60">
                  BIO
                </p>

                <div
                  className="
                    font-mono text-xs leading-relaxed text-muted-foreground text-justify
                    max-h-40 overflow-y-auto
                    p-3 pr-4
                    scroll-py-3
                    scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent

                    [&_h1]:mt-2 [&_h1]:mb-2 [&_h1]:text-base [&_h1]:font-arcade [&_h1]:tracking-widest [&_h1]:text-primary
                    [&_h2]:mt-2 [&_h2]:mb-2 [&_h2]:text-sm [&_h2]:font-arcade [&_h2]:tracking-wider [&_h2]:text-secondary
                    [&_h3]:mt-2 [&_h3]:mb-1 [&_h3]:text-xs [&_h3]:font-semibold

                    [&_p]:mb-2

                    [&_ul]:list-disc [&_ul]:ml-5 [&_ul]:mb-2
                    [&_ol]:list-decimal [&_ol]:ml-5 [&_ol]:mb-2
                    [&_li]:mb-1

                    [&_blockquote]:border-l-2 [&_blockquote]:border-primary/40
                    [&_blockquote]:pl-3 [&_blockquote]:italic [&_blockquote]:text-muted-foreground/80

                    [&_code]:bg-background [&_code]:px-1.5 [&_code]:py-0.5
                    [&_code]:rounded [&_code]:text-[11px] [&_code]:text-primary

                    [&_pre]:bg-background [&_pre]:p-3 [&_pre]:rounded
                    [&_pre]:overflow-x-auto [&_pre]:mb-2

                    [&_a]:text-primary [&_a]:underline [&_a]:underline-offset-2

                    [&_hr]:my-3 [&_hr]:border-border/40

                    [&_table]:w-full [&_table]:border-collapse [&_table]:mb-3
                    [&_th]:border [&_th]:border-border/40 [&_th]:px-2 [&_th]:py-1 [&_th]:text-left
                    [&_td]:border [&_td]:border-border/40 [&_td]:px-2 [&_td]:py-1

                    [&_img]:max-w-full [&_img]:rounded [&_img]:my-2
                  "
                  dangerouslySetInnerHTML={{ __html: html }}
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* ================= PROBLEMS ================= */}
        <div className="lg:col-span-2">
          <Card className="border-border/50 bg-card/50 pixel-card pixel-scanlines">
            <CardHeader className="pb-0">
              <Tabs
                value={activeTab}
                onValueChange={v => setActiveTab(v as any)}
              >
                <TabsList className="grid w-full grid-cols-2 bg-background/50 p-1">
                  <TabsTrigger
                    value="solved"
                    className="gap-2 font-arcade text-xs arcade-tab"
                  >
                    <CheckCircle className="h-4 w-4" />
                    Resolvidos
                  </TabsTrigger>

                  <TabsTrigger
                    value="created"
                    className="gap-2 font-arcade text-xs arcade-tab"
                  >
                    <Lightbulb className="h-4 w-4" />
                    Criados
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </CardHeader>

            <CardContent className="pt-4">
              <Tabs value={activeTab}>
                <TabsContent value="solved">
                  {solvedProblems.length ? (
                    <div className="space-y-2">
                      {solvedProblems.map(p => (
                        <Link
                          key={p.id}
                          to={`/problem/${p.id}`}
                          className="flex justify-between items-center p-3 rounded-lg bg-background/50 arcade-list-item"
                        >
                          <div className="flex items-center gap-3">
                            <span className="font-mono text-muted-foreground">
                              #{p.id}
                            </span>
                            <span>{p.title}</span>
                            <DifficultyBadge difficulty={p.difficulty} />
                          </div>

                          <span className="font-pixel text-[8px] text-neon-green">
                            ACEITO
                          </span>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <EmptyState
                      icon={Gamepad2}
                      title="NENHUM PROBLEMA RESOLVIDO"
                      text="Este usuário ainda não resolveu nenhum problema."
                    />
                  )}
                </TabsContent>

                <TabsContent value="created">
                  {createdProblems.length ? (
                    <div className="space-y-2">
                      {createdProblems.map(p => (
                        <Link
                          key={p.id}
                          to={`/problem/${p.id}`}
                          className="flex justify-between items-center p-3 rounded-lg bg-background/50 arcade-list-item"
                        >
                          <div className="flex items-center gap-3">
                            <span className="font-mono text-muted-foreground">
                              #{p.id}
                            </span>
                            <span>{p.title}</span>
                            <DifficultyBadge difficulty={p.difficulty} />
                          </div>

                          <span className="text-sm text-muted-foreground">
                            {p.solved} soluções
                          </span>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <EmptyState
                      icon={Lightbulb}
                      title="NENHUM PROBLEMA CRIADO"
                      text="Este usuário ainda não criou nenhum problema."
                    />
                  )}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageContainer>
  )
}

/* ================= EMPTY STATE ================= */
function EmptyState({
  icon: Icon,
  title,
  text,
}: {
  icon: any
  title: string
  text: string
}) {
  return (
    <div className="text-center py-12">
      <Icon className="h-16 w-16 mx-auto text-muted-foreground/50 mb-4" />
      <p className="font-pixel text-[10px] text-muted-foreground mb-2">
        {title}
      </p>
      <p className="text-sm text-muted-foreground">{text}</p>
    </div>
  )
}
