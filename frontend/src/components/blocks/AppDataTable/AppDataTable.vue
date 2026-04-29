<template>
  <div :class="$style.wrap">
    <table :class="$style.table">
      <thead>
        <tr>
          <th
            v-for="column in columns"
            :key="column.key"
            :class="[
              $style.headCell,
              column.align === 'center' && $style.alignCenter,
              column.align === 'right' && $style.alignRight,
            ]"
          >
            {{ column.label }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-if="rows.length === 0">
          <td :colspan="columns.length" :class="$style.empty">
            <slot name="empty">
              Нет данных.
            </slot>
          </td>
        </tr>

        <tr
          v-for="row in rows"
          v-else
          :key="getRowKey(row)"
          :class="[$style.row, getRowToneClass(row)]"
        >
          <td
            v-for="column in columns"
            :key="column.key"
            :class="[
              $style.cell,
              column.align === 'center' && $style.alignCenter,
              column.align === 'right' && $style.alignRight,
            ]"
          >
            <slot
              :name="`cell-${column.key}`"
              :row="row"
              :value="row[column.key]"
              :column="column"
            >
              {{ row[column.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useCssModule } from 'vue'

const props = defineProps({
  columns: {
    type: Array,
    default: () => [],
  },
  rows: {
    type: Array,
    default: () => [],
  },
  rowKey: {
    type: [String, Function],
    default: 'id',
  },
  rowToneKey: {
    type: String,
    default: '',
  },
})

const style = useCssModule()

const getRowKey = (row) => {
  if (typeof props.rowKey === 'function') {
    return props.rowKey(row)
  }

  return row?.[props.rowKey] ?? JSON.stringify(row)
}

const getRowToneClass = (row) => {
  if (!props.rowToneKey) {
    return ''
  }

  const tone = row?.[props.rowToneKey]

  if (!tone) {
    return ''
  }

  return {
    subtle: style.rowSubtle,
    success: style.rowSuccess,
    warning: style.rowWarning,
    danger: style.rowDanger,
  }[tone] || ''
}
</script>

<style module lang="scss" src="./AppDataTable.module.scss"></style>
