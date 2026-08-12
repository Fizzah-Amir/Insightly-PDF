import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ReactFlow, { Background, Controls, MiniMap } from "reactflow";
import type { Node, Edge } from "reactflow";
import "reactflow/dist/style.css";
import { Share2 } from "lucide-react";
import api from "../api/axios";

interface Concept {
  id: number;
  name: string;
  page_number: number;
}

function MindMap() {
  const { id } = useParams();
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMindMap();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const loadMindMap = async () => {
    try {
      const response =  await api.get(`http://127.0.0.1:8000/api/questions/mindmap/${id}/`);
      const concepts: Concept[] = response.data.concepts;
      const relationships = response.data.relationships;

      const generatedNodes = concepts.map((concept: Concept, index: number) => ({
        id: String(concept.id),
        position: { x: (index % 4) * 250, y: Math.floor(index / 4) * 150 },
        data: { label: `${concept.name}\n(p. ${concept.page_number + 1})` },
        style: {
          background: "#4338ca",
          color: "white",
          padding: 14,
          borderRadius: 12,
          width: 160,
          textAlign: "center" as const,
          fontFamily: "Inter, sans-serif",
          fontSize: 13,
          border: "none",
        },
      }));

      const generatedEdges = relationships.map((rel: any) => ({
        id: String(rel.id),
        source: String(rel.from_concept_id),
        target: String(rel.to_concept_id),
        label: rel.relationship,
        animated: true,
        style: { stroke: "#0e8e82" },
        labelStyle: { fill: "#6d6a72", fontFamily: "JetBrains Mono, monospace", fontSize: 11 },
      }));

      setNodes(generatedNodes);
      setEdges(generatedEdges);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-72px-72px)]">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Knowledge mind map</h1>
          <p className="text-ink-soft mt-1">How the concepts in this document relate to each other.</p>
        </div>
      </div>

      {loading ? (
        <div className="h-[calc(100%-4rem)] rounded-2xl border border-line bg-surface flex flex-col items-center justify-center gap-3">
          <Share2 size={28} className="text-ink-faint animate-pulse" />
          <p className="text-ink-soft text-sm">Generating mind map…</p>
        </div>
      ) : nodes.length === 0 ? (
        <div className="h-[calc(100%-4rem)] rounded-2xl border border-line bg-surface flex flex-col items-center justify-center gap-2 text-center px-6">
          <Share2 size={28} className="text-ink-faint" />
          <p className="text-ink font-medium mt-2">No concepts extracted yet</p>
          <p className="text-ink-soft text-sm max-w-xs">
            This document hasn't finished processing, or has no concepts to map.
          </p>
        </div>
      ) : (
        <div className="h-[calc(100%-4rem)] rounded-2xl border border-line overflow-hidden bg-surface">
          <ReactFlow nodes={nodes} edges={edges} fitView>
            <Background color="#e4e1d8" gap={20} />
            <Controls />
            <MiniMap nodeColor="#4338ca" maskColor="rgba(245,243,238,0.7)" />
          </ReactFlow>
        </div>
      )}
    </div>
  );
}

export default MindMap;
