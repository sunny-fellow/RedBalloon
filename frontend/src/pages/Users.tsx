import { useState } from 'react';
import { PageContainer } from '@/components/layout/PageContainer';
import { UserCard } from '@/components/cards/UserCard';
import { SearchFilters } from '@/components/common/SearchFilters';
import { Pagination } from '@/components/common/Pagination';
import { mockUsers, countries } from '@/data/mockData';

export default function Users() {
  const [search, setSearch] = useState('');
  const [country, setCountry] = useState('');
  const [page, setPage] = useState(1);
  return (
    <PageContainer>
      <h1 className="text-3xl font-bold mb-6 gradient-text">Usuários</h1>
      <SearchFilters
        searchPlaceholder="Buscar por nome..."
        searchValue={search}
        onSearchChange={setSearch}
        filters={[{ key: 'country', label: 'País', options: countries.map(c => ({ value: c, label: c })), value: country, onChange: setCountry }]}
        onClearFilters={() => { setSearch(''); setCountry(''); }}
      />
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mt-6">
        {mockUsers.map(u => <UserCard key={u.id} user={u} />)}
      </div>
      <div className="mt-8"><Pagination currentPage={page} totalPages={3} onPageChange={setPage} /></div>
    </PageContainer>
  );
}
