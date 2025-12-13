import { Search, Filter, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { TagBadge } from '@/components/ui/TagBadge';

interface FilterOption {
  value: string;
  label: string;
}

interface SearchFiltersProps {
  searchPlaceholder?: string;
  searchValue: string;
  onSearchChange: (value: string) => void;
  filters?: {
    key: string;
    label: string;
    options: FilterOption[];
    value: string;
    onChange: (value: string) => void;
  }[];
  tags?: {
    name: string;
    color: 'cyan' | 'purple' | 'pink' | 'green' | 'orange' | 'yellow';
  }[];
  selectedTags?: string[];
  onTagSelect?: (tag: string) => void;
  onClearFilters?: () => void;
}

export function SearchFilters({
  searchPlaceholder = 'Buscar...',
  searchValue,
  onSearchChange,
  filters = [],
  tags = [],
  selectedTags = [],
  onTagSelect,
  onClearFilters,
}: SearchFiltersProps) {
  const hasActiveFilters = searchValue || selectedTags.length > 0 || filters.some(f => f.value);

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder={searchPlaceholder}
            value={searchValue}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-10 bg-card/50 border-border/50 focus:border-primary"
          />
        </div>

        {filters.map((filter) => (
          <Select key={filter.key} value={filter.value} onValueChange={filter.onChange}>
            <SelectTrigger className="w-full sm:w-[180px] bg-card/50 border-border/50">
              <SelectValue placeholder={filter.label} />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              {filter.options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        ))}

        {hasActiveFilters && onClearFilters && (
          <Button variant="ghost" size="icon" onClick={onClearFilters}>
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          <Filter className="h-4 w-4 text-muted-foreground mt-1" />
          {tags.map((tag) => (
            <TagBadge
              key={tag.name}
              tag={tag.name}
              color={tag.color}
              onClick={() => onTagSelect?.(tag.name)}
              selected={selectedTags.includes(tag.name)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
