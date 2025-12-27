import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowLeft,
  CheckCircle,
  Target,
  Edit2,
  Lightbulb,
  Gamepad2,
  Image as ImageIcon,
} from 'lucide-react';

import { PageContainer } from '@/components/layout/PageContainer';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DifficultyBadge } from '@/components/ui/DifficultyBadge';
import { currentUser, mockProblems } from '@/data/mockData';
import { Textarea } from '@/components/ui/textarea';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

import AvatarSeeds from '@/types/avatars';

const avatarUrl = (seed: string) =>
  `https://api.dicebear.com/9.x/adventurer/svg?seed=${seed}`;

export default function Profile() {
  const [activeTab, setActiveTab] = useState('solved');
  const [avatarModalOpen, setAvatarModalOpen] = useState(false);
  const [avatarSeed, setAvatarSeed] = useState(AvatarSeeds[0]);

  const solvedProblems = mockProblems.slice(0, 3);
  const createdProblems = mockProblems.filter(
    (p) => p.creatorId === currentUser.id,
  );

  return (
    <PageContainer>
      <Link to="/home">
        <Button variant="ghost" className="mb-4 gap-2">
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
      </Link>

      <div className="grid lg:grid-cols-3 gap-6 items-start">
        {/* PROFILE */}
        <Card className="lg:col-span-1 border-border/50 bg-card/50 pixel-card h-fit">
          <CardContent className="pt-6 text-center space-y-4">
            <div className="relative w-fit mx-auto">
              <button
                onClick={() => setAvatarModalOpen(true)}
                className="group"
              >
                <Avatar className="h-24 w-24 ring-4 ring-primary/30">
                  <AvatarImage src={avatarUrl(avatarSeed)} />
                  <AvatarFallback>
                    {currentUser.name.charAt(0)}
                  </AvatarFallback>
                </Avatar>

                <div className="absolute inset-0 rounded-full bg-black/50 opacity-0 group-hover:opacity-100 transition flex items-center justify-center">
                  <ImageIcon className="h-6 w-6 text-white" />
                </div>
              </button>
            </div>

            <div className="space-y-1">
              <h2 className="text-xl font-arcade font-bold text-glow-purple text-flicker">
                {currentUser.name}
              </h2>
              <p className="text-muted-foreground font-mono text-sm">
                @{currentUser.login}
              </p>
            </div>

            <div className="space-y-3 pt-2">
              <Input
                defaultValue={currentUser.name}
                className="bg-background/50"
              />
              <Textarea
                defaultValue={currentUser.description}
                className="bg-background/50 resize-none"
              />
            </div>

            <Button className="w-full gap-2 pixel-btn">
              <Edit2 className="h-4 w-4" />
              Salvar Alterações
            </Button>
          </CardContent>
        </Card>

        {/* STATS + TABS */}
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <Card className="border-border/50 bg-card/50 pixel-card arcade-hover-card">
              <CardContent className="pt-6 text-center">
                <Target className="h-8 w-8 mx-auto text-neon-orange" />
                <p className="text-3xl font-arcade font-bold mt-2 text-glow-pink">
                  {currentUser.problemsAttempted}
                </p>
                <p className="text-muted-foreground font-pixel text-[8px] mt-1">
                  TENTADOS
                </p>
              </CardContent>
            </Card>

            <Card className="border-border/50 bg-card/50 pixel-card arcade-hover-card">
              <CardContent className="pt-6 text-center">
                <CheckCircle className="h-8 w-8 mx-auto text-neon-green" />
                <p className="text-3xl font-arcade font-bold mt-2 text-glow-cyan">
                  {currentUser.problemsSolved}
                </p>
                <p className="text-muted-foreground font-pixel text-[8px] mt-1">
                  RESOLVIDOS
                </p>
              </CardContent>
            </Card>
          </div>

          {/* TABS */}
          <Card className="border-border/50 bg-card/50 pixel-card pixel-scanlines">
            <CardHeader className="pb-0">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className="grid w-full grid-cols-2 bg-background/50 p-1">
                  <TabsTrigger
                    value="solved"
                    className="gap-2 font-arcade text-xs"
                  >
                    <CheckCircle className="h-4 w-4" />
                    Resolvidos
                  </TabsTrigger>
                  <TabsTrigger
                    value="created"
                    className="gap-2 font-arcade text-xs"
                  >
                    <Lightbulb className="h-4 w-4" />
                    Criados
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </CardHeader>

            <CardContent className="pt-4">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsContent value="solved" className="mt-0">
                  {solvedProblems.map((p) => (
                    <Link
                      key={p.id}
                      to={`/problem/${p.id}`}
                      className="flex justify-between items-center p-3 rounded-lg bg-background/50 arcade-list-item"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-muted-foreground font-mono">
                          #{p.id}
                        </span>
                        <span>{p.title}</span>
                        <DifficultyBadge difficulty={p.difficulty} />
                      </div>
                      <span className="text-neon-green font-pixel text-[8px]">
                        ACEITO
                      </span>
                    </Link>
                  ))}
                </TabsContent>

                <TabsContent value="created" className="mt-0">
                  {createdProblems.map((p) => (
                    <Link
                      key={p.id}
                      to={`/problem/${p.id}`}
                      className="flex justify-between items-center p-3 rounded-lg bg-background/50 arcade-list-item"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-muted-foreground font-mono">
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
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* AVATAR MODAL */}
      <Dialog open={avatarModalOpen} onOpenChange={setAvatarModalOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Escolha seu avatar</DialogTitle>
          </DialogHeader>

          <div className="grid grid-cols-6 gap-4 mt-4">
            {AvatarSeeds.map((seed) => (
              <button
                key={seed}
                onClick={() => {
                  setAvatarSeed(seed);
                  setAvatarModalOpen(false);
                }}
                className={`
                  rounded-full p-1 transition flex items-center justify-center
                  border border-white/15 bg-white/5
                  ${
                    avatarSeed === seed
                      ? 'ring-2 ring-primary border-primary/60'
                      : 'hover:border-white/30 hover:bg-white/10'
                  }
                `}
              >
                <img
                  src={avatarUrl(seed)}
                  alt={seed}
                  className="w-15 h-15 rounded-full"
                />
              </button>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </PageContainer>
  );
}
